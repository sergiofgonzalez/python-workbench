In Node.js, there's a prod-grade library by Sindre Sorhus called [p-limit](https://github.com/sindresorhus/p-limit) that implements limited parallel concurrency with a great DX:

```javascript
import pLimit from 'p-limit';

const limit = pLimit(1);

const input = [
	limit(() => fetchSomething('foo')),
	limit(() => fetchSomething('bar')),
	limit(() => doSomething())
];

// Only one promise is run at once
const result = await Promise.all(input);
console.log(result);
```

Enhance the `WorkQueue` previous implementation, so that it features the same developer experience.
HINT: use an async context manager.


