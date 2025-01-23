# Request builder

Create your own builder class around [`requests`](https://github.com/psf/requests). The builder must be able to provide at least basic facilities to specify the HTTP method, the URL, the query component of the URL, the header parameters, and the eventual body data to be sent.

To send the request, provide and `invoke()` method that returns the result for the invocation.

| NOTE: |
| :---- |
| The idea is exercise the way in which the Builder pattern is used! |