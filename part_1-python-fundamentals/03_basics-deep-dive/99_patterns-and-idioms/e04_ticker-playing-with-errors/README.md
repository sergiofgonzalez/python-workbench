# Ticker: playing with errors

Modify the function created in the previous exercise ([A simple modification](e03_ticker-simple-modification/)) to produce an error if the timestamp at the moment of a tick (including the one emitted at the beginning) is divisible by 5. Propagate the error using both the callback and the event emitter and handle the error correctly.