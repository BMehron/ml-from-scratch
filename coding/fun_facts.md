A Famous Example

These two loops compute the same thing.

Fast version
for i in range(N):
    sum += array[i]

Memory accessed sequentially → great cache usage.

Slow version
for i in range(N):
    sum += array[random_index[i]]

Memory accessed randomly → cache misses.

The second version can be 10–100× slower.

Same math, different memory behavior.


Cache Is Why Matrix Layout Matters

Example:

Matrix stored row-major.

Fast:

for i:
  for j:
    A[i][j]

Slow:

for j:
  for i:
    A[i][j]

The second version jumps around memory → bad cache usage.


1️⃣ RAM Doesn't Return Single Numbers

When the CPU reads memory, it does not fetch just one value.

Instead it loads a cache line.

Typical size:

64 bytes

Example:

If you read:

array[100]

the CPU actually loads something like:

array[96 ... 111]

(64 bytes worth of data)

That block is stored in cache.

So future reads of nearby values are already available instantly.

2️⃣ Sequential Access Uses the Whole Cache Line

Consider this loop:

for i in range(N):
    sum += array[i]

Step-by-step:

CPU loads cache line containing array[0..15]

CPU uses all values already in cache

Then loads next cache line

Repeat

So each RAM fetch is fully utilized.

Example:

1 RAM access → 16 integers used

This is very efficient.

3️⃣ Random Access Wastes Most of the Cache Line

Now consider:

for i in range(N):
    sum += array[random_index[i]]

Each access may be far apart in memory.

Example:

array[3]
array[900000]
array[42]
array[1000000]

Each time the CPU must:

fetch a full 64-byte cache line

but only 1 value is used.

Example:

1 RAM access → only 1 integer used

The other 15 values are wasted.

So memory bandwidth is used inefficiently.