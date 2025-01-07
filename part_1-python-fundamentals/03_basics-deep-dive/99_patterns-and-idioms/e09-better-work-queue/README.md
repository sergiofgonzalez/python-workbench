# A better WorkQueue

WorkQueue implementation has an obvious flaw: it is impossible to get the result of a work item you process using the work queue.

Create a better version of the `WorkQueue` class that allows you get the result of each individual work item you send to the queue (if you're interested). Otherwise, you can simply discard the result and the program should keep working as it was working before.

## workqueue_v1: first approach

Works OK, but requires the client code to keep track of the enqueueing.

## workqueue_v2: better approach

A better approach in which the client code should just take care of calling the `work_queue.run_work(fn)` and keeping track of the resulting `Future`.

Note that this "better queue" is slower than the previous implementation, because there are more tasks created for enqueueing.