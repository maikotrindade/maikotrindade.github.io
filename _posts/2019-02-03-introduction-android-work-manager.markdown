---
published: true
title: "Android WorkManager: A Practical Guide to Background Work"
layout: post
last_modified_at: 2026-11-17
tags: [Android, WorkManager, Kotlin, Coroutines, BackgroundWork, Jetpack]
description: "Android WorkManager in Kotlin: CoroutineWorker, constraints, unique and periodic work, chaining, expedited jobs, observing progress and testing."
---

WorkManager is the Jetpack library for background work that must finish even if the user leaves the app or the device restarts: uploading a photo, syncing data, sending logs. You describe the work and the conditions it needs (network, charging, enough storage), and WorkManager decides when to run it, retries it if it fails, and survives process death and reboots. This guide covers the APIs you'll use in a modern Kotlin app.

I first wrote about WorkManager in 2019, when version 2.0 was new and examples were in Groovy with JCenter. I've rewritten the post for current WorkManager with coroutines.

## When to use WorkManager

Android has several ways to do work off the main thread, and picking the wrong one causes most background bugs:

| Situation | Use |
|---|---|
| Work tied to a screen (load data while it's visible) | Coroutines in `viewModelScope` |
| Work that must complete even if the app closes, and can wait for the right conditions | **WorkManager** |
| Work the user started and is watching right now (a long download, a workout) | A foreground service, or WorkManager long-running work |
| Something at an exact time (an alarm clock, a calendar reminder) | `AlarmManager` exact alarms |

WorkManager is about **guaranteed**, **deferrable** work. It's not for things that must happen at a precise second, and it's not a replacement for coroutines inside a screen.

## Setup

Add the KTX artifact, which includes coroutine support:

```kotlin
// build.gradle.kts (app module)
dependencies {
    implementation("androidx.work:work-runtime-ktx:<latest-version>")
    androidTestImplementation("androidx.work:work-testing:<latest-version>")
}
```

Check the <a href="https://developer.android.com/jetpack/androidx/releases/work" target="_blank" rel="noopener noreferrer" title="WorkManager release notes">release notes</a> for the current version. WorkManager initializes itself on app start, so for most apps there's nothing else to configure.

## Writing a worker

Extend **`CoroutineWorker`** and put the work in `doWork()`, which is a suspend function. It runs on `Dispatchers.Default` by default, and you can call other suspend functions directly:

```kotlin
class UploadPhotoWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        val uri = inputData.getString(KEY_URI) ?: return Result.failure()
        return try {
            val url = PhotoApi.upload(Uri.parse(uri))
            Result.success(workDataOf(KEY_URL to url))
        } catch (e: IOException) {
            if (runAttemptCount < 3) Result.retry() else Result.failure()
        }
    }

    companion object {
        const val KEY_URI = "uri"
        const val KEY_URL = "url"
    }
}
```

The return value tells WorkManager what happened:

- `Result.success()` means done, optionally with output data.
- `Result.retry()` means try again later, using the backoff policy.
- `Result.failure()` means give up. Work chained after this one is cancelled too.

`inputData` and output data are small key-value maps, limited to 10 KB. Pass IDs or URIs, not the content itself.

## Scheduling work

### One-time work with constraints

```kotlin
val request = OneTimeWorkRequestBuilder<UploadPhotoWorker>()
    .setInputData(workDataOf(UploadPhotoWorker.KEY_URI to photoUri.toString()))
    .setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.UNMETERED)
            .setRequiresBatteryNotLow(true)
            .build()
    )
    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)
    .addTag("photo-upload")
    .build()

WorkManager.getInstance(context).enqueue(request)
```

The upload waits until the device is on Wi-Fi with a healthy battery, then runs. If it returns `retry()`, WorkManager waits 30 seconds, then 60, then 120, and so on.

### Unique work

If a user taps "sync" five times, you don't want five syncs. **Unique work** gives a job a name and lets you decide what happens on conflict:

```kotlin
WorkManager.getInstance(context).enqueueUniqueWork(
    "sync",
    ExistingWorkPolicy.KEEP, // ignore the new request if one is pending or running
    OneTimeWorkRequestBuilder<SyncWorker>().build()
)
```

`REPLACE` cancels the existing work and starts the new one, and `APPEND_OR_REPLACE` queues the new work after the existing one.

### Periodic work

```kotlin
val dailySync = PeriodicWorkRequestBuilder<SyncWorker>(1, TimeUnit.DAYS)
    .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())
    .build()

WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "daily-sync",
    ExistingPeriodicWorkPolicy.KEEP,
    dailySync
)
```

The minimum interval is 15 minutes, and the exact run time is flexible: Android batches work to save battery. Always enqueue periodic work as unique work. Otherwise every app start adds another copy.

### Chaining

Run work in sequence, passing each worker's output to the next as input:

```kotlin
WorkManager.getInstance(context)
    .beginWith(listOf(compressPhoto1, compressPhoto2)) // these two run in parallel
    .then(uploadAll)
    .then(cleanUp)
    .enqueue()
```

If any step fails, the steps after it are cancelled.

## Expedited and long-running work

For short, important work the user is waiting on, like sending a message, mark the request as **expedited**:

```kotlin
val send = OneTimeWorkRequestBuilder<SendMessageWorker>()
    .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
    .build()
```

Expedited work starts as soon as possible, but it's subject to a system quota. The out-of-quota policy says what to do when the quota runs out. On Android 11 and lower, expedited work runs as a foreground service, so your worker should override `getForegroundInfo()` to provide the notification.

For work that runs for minutes, like a large download, call `setForeground()` from inside `doWork()` so the system keeps it alive and the user sees a notification. On Android 14 and up, the foreground service type must also be declared in the manifest.

## Observing progress and results

Every request has an ID, and WorkManager exposes its state as a `Flow`:

```kotlin
WorkManager.getInstance(context)
    .getWorkInfoByIdFlow(request.id)
    .collect { info ->
        when (info?.state) {
            WorkInfo.State.RUNNING -> showProgress(info.progress.getInt("percent", 0))
            WorkInfo.State.SUCCEEDED -> showDone(info.outputData.getString(UploadPhotoWorker.KEY_URL))
            WorkInfo.State.FAILED -> showError()
            else -> Unit
        }
    }
```

Inside the worker, report progress with `setProgress(workDataOf("percent" to 40))`. You can also observe all work with a tag (`getWorkInfosByTagFlow`) or a unique name (`getWorkInfosForUniqueWorkFlow`). To stop work, call `cancelWorkById`, `cancelAllWorkByTag` or `cancelUniqueWork`.

## Testing workers

The `work-testing` artifact lets you run a worker directly in a test, without scheduling it:

```kotlin
@Test
fun upload_withoutUri_fails() = runTest {
    val worker = TestListenableWorkerBuilder<UploadPhotoWorker>(
        context = ApplicationProvider.getApplicationContext()
    ).build()

    assertEquals(ListenableWorker.Result.failure(), worker.doWork())
}
```

For end-to-end checks of constraints and delays, `WorkManagerTestInitHelper` gives you a test driver that can mark constraints as met and skip initial delays.

## Common mistakes

- **Using WorkManager for exact timing.** It may run your work minutes or hours later. Use `AlarmManager` for exact times.
- **Enqueueing periodic work on every app start** without `enqueueUniquePeriodicWork`.
- **Passing large data in `inputData`.** Store it in a file or database and pass the ID.
- **Ignoring `isStopped`.** The system can stop a worker when constraints are no longer met. `CoroutineWorker` cancels the coroutine, so make long loops check for cancellation (see my <a href="https://maikotrindade.com/2020/02/20/coroutines-android-simplify-code.html" target="_blank" rel="noopener" title="Kotlin coroutines on Android guide">coroutines guide</a> on cooperative cancellation).
- **Holding references to Activities or Views in a worker.** Workers outlive your UI.

Android's <a href="https://developer.android.com/develop/background-work/background-tasks/persistent" target="_blank" rel="noopener noreferrer" title="Persistent work with WorkManager, Android Developers">WorkManager guide</a> covers advanced topics like custom initialization, multi-process apps and RxJava workers.
