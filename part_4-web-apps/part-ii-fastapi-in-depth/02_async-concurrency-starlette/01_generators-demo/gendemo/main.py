"""Simple example illustrating generators"""


def get_lines():
    yield "Han Solo: Uh, everything's under control. Situation normal."
    yield "Control: What happened?"
    yield (
        "Han Solo: Uh, we had a slight weapons malfunction, but uh... "
        "everything's perfectly all right now. We're fine. We're all fine "
        "here now, thank you. How are you?"
    )
    yield "Control: We're sending a squad up"
    yield (
        "Han Solo: Uh, uh... negative, negative. We had a reactor leak here "
        "now. Give us a few minutes to lock it down. Large leak, very "
        "dangerous."
    )
    yield "Control: Who is this? What's your operating number?"
    yield "Han Solo: Uh..."
    yield (
        "Han Solo: Boring conversation anyway. Luke, we're gonna have "
        "company!"
    )


# Note that you cannot invoke a generator function as a regular function
print(doh())

# It has to be invoked in an iteration context
for line in doh():
    print(line)
