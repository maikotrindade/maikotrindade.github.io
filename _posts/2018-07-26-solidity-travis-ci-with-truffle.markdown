---
published: true
title: Solidity – Travis CI with Truffle
layout: post
---

### Continuous Integration
[Continuous Integration] aka _CI_ is a development practice that requires developers to integrate code into a shared repository several times a day. Each check-in is then verified by an automated build, allowing teams to detect problems early. By integrating regularly, you can detect errors quickly, and locate them more easily and not integrating continuously you will have longer periods between integrations. This makes it exponentially more difficult to find and fix problems. Such integration problems can easily knock a project off-schedule, or cause it to fail altogether.

<img src="https://maikotrindade.com/public/img/ci.png" width="380" height="290" alt="Continuous Integration"/>


### Travis CI
Using [Travis CI], the users can easily sync [Github] projects and test the code test the code in minutes. Travis CI can be configured to run the tests on a range of different machines, with different software installed (such as older versions of a programming language implementation, to test for compatibility), and supports building software in numerous languages, including C, C++, C#, Clojure, D, Erlang, F#, Go, Apache Groovy, Haskell, Java, JavaScript, Julia, Perl, PHP, Python, R, Ruby, Rust, Scala and Visual Basic. Several high-profile open source projects are using it to run builds and tests on every commit, such as Plone, Ruby on Rails, and Ruby.[8][9

### Truffle with Travis CI
Firstly, as prerequisite you should follow the Travis CI docs in order to integrate your Github project with Travis.
Then add the following chunk of code into your `.travis.yml`:

<script src="https://gist.github.com/maikotrindade/2d544de08215085abfbba59ce3378a2c.js"></script>

In this script, we are selecting nodeJs version 8.11.3 with latest version of Node package manager (npm). Ganache (old testRPC) and truffle are also installed. The trigger mechanisms starts with ganache initialization and the truffle command `truffle test`.  In other words, the code will be compiled and the tests will ran too.

[Continuous Integration]: https://www.thoughtworks.com/continuous-integration
[Github]: https://github.com
[Travis CI]: https://travis-ci.com
[Travis CI docs]: https://docs.travis-ci.com/user/getting-started/