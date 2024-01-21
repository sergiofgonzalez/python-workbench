"""ASync example"""
import asyncio


async def q():
    print("Why can't programmers tell jokes?")
    await asyncio.sleep(3)
    print("\t==> q() done")


async def a():
    print("Timing!")
    print("\t==> a() done")


async def main():
    await asyncio.gather(q(), a())
    print("\t==> main() done")


if __name__ == "__main__":
    asyncio.run(main())
    print("\t==> program done")
