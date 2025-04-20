# Parallel Image Processor

Demonstrates how using a ParallelFlow with a Trigger Node processes multiple images with multiple filters >8x faster than a sequential Flow.

## Features

```mermaid
graph TD
    A[Trigger Image Processing] --> B(ParallelFlow)
    subgraph B [Parallel Image Processing Flow]
        subgraph C [Per Image-Filter Flow]
            D[Load Image] --> E[Apply Filter]
            E --> F[Save Image]
        end
    end
    B --> G[Aggregation (Optional)]
```

- Processes images with multiple filters in parallel using a Trigger Node and ParallelFlow
- Applies three different filters (grayscale, blur, sepia)
- Shows significant speed improvement over sequential processing
- Manages system resources with semaphores

## Run It

```bash
pip install -r requirements.txt
python main.py
```

## Output

```=== Processing Images in Parallel ===
Parallel Image Processor
------------------------------
Found 3 images:
- images/bird.jpg
- images/cat.jpg
- images/dog.jpg

Running sequential flow...
Processing 3 images with 3 filters...
Total combinations: 9
Trigger: Triggering summary for 9 files.
Processor: Summarizing images/bird.jpg (Index 0)...
Saved: output/bird_grayscale.jpg
...etc

Timing Results:
Sequential processing: 13.76 seconds
Parallel processing: 1.71 seconds
Speedup: 8.04x

Processing complete! Check the output/ directory for results.
```

## Key Points

- **Sequential Flow**: Total time = sum of all item times

  - Good for: Rate-limited APIs, maintaining order

- **Parallel Flow**: Total time ≈ longest single item time
  - Good for: I/O-bound tasks, independent operations
