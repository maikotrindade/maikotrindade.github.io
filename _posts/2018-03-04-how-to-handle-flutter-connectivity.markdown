---
published: true
title: How to handle Flutter connectivity
layout: post
---

A profissional app handles offline/online connectivity in order to interact with the user according to his phone state. 
A [Flutter] could not be different and in this post I will you an amazing library which will facilitate our development.
The [flutter_offline] developed by [jogboms] is an utility library for handling offline/online connectivity. 

### Installation and Usage

The process is really straightforward. First of all, you need to add the library's dependency in your project:

`dependencies:
  flutter_offline: "^0.2.1"`

Next step is import the package that you included in you project and start using the library as the following example shows:

<script src="https://gist.github.com/maikotrindade/11bf4e8c34881f74db35f22ff724ebd2.js"></script>

[Flutter]: https://flutter.io/
[flutter_offline]: https://github.com/jogboms/flutter_offline
[jogboms]: https://github.com/jogboms
