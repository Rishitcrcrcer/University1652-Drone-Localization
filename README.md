# University-1652 Drone Image Localization

A computer vision project for matching drone-view images with satellite-view gallery images using cross-view image retrieval.

## Overview

The goal of this project is to identify the most likely satellite image corresponding to a given drone image. The predicted gallery ID can then be mapped to geographic coordinates to estimate the image's location.

The project uses a pretrained cross-view image matching model and evaluates its retrieval performance across the University-1652 dataset.

## Problem Statement

Drone images and satellite images capture the same locations from very different viewpoints. Matching these images is challenging because of changes in perspective, scale, orientation, and visible scene features.

This project evaluates a baseline approach for retrieving the closest matching satellite image for each drone query.

## Methodology

1. Load the pretrained cross-view retrieval model.
2. Extract and load image feature representations.
3. Normalize the feature vectors.
4. Compute cosine similarity between each drone query and all satellite gallery images.
5. Rank gallery images by similarity and select the top-ranked match.
6. Map predicted and ground-truth gallery IDs to latitude and longitude using coordinate data.
7. Evaluate retrieval accuracy and geographic localization error.

## Dataset and Evaluation

- Drone query images: 37,855
- Satellite gallery images: 951
- Query identity folders: 701
- Gallery IDs with coordinate entries: 951

## Results

### Image Retrieval Performance

| Metric | Result |
|---|---:|
| Recall@1 | 58.25% |
| Recall@5 | 78.38% |
| Recall@10 | 85.13% |

Recall@K measures how often the correct gallery identity appears among the top K retrieved candidates.

### Geographic Localization Error

| Metric | Result |
|---|---:|
| Mean error | 628.63 km |
| Median error | 0 km |
| 90th-percentile error | 2,513.11 km |
| 95th-percentile error | 3,876.38 km |

The geographic results show that many queries have zero reported error, while incorrect top-1 matches can produce very large errors. The coordinate mappings and evaluation assumptions still require independent validation, so these results should be treated as preliminary.

## Repository Structure

```text
University1652-Drone-Localization/
├── README.md
├── evaluate_localization.py
├── localization_summary.txt
├── localization_evaluation.csv   # Optional; may be large
├── requirements.txt
└── .gitignore
```

The pretrained model, extracted features, original dataset, and coordinate data are not included in this repository by default.

## Requirements

- Python 3
- PyTorch
- NumPy
- pandas
- SciPy

Additional dependencies may be required by the original baseline model. Use compatible package versions for the baseline code and checkpoint.

## Running the Evaluation

1. Obtain the dataset and pretrained checkpoint through their permitted distribution sources.
2. Set up the Python environment and install the required dependencies.
3. Extract or generate the model features using the baseline pipeline, if they are not already available.
4. Configure the paths in `evaluate_localization.py` to point to your local feature file and coordinate CSV.
5. Run:

```bash
python evaluate_localization.py
```

The evaluation generates per-query retrieval predictions and geographic error statistics.

## Limitations

- The reported results come from a baseline evaluation and not a newly trained or fine-tuned model.
- Coordinate mappings have not been independently verified for every identity.
- Incorrect top-1 matches can result in substantial geographic localization errors.
- Results depend on the pretrained checkpoint, feature extraction pipeline, and correctness of the coordinate mapping.

## Future Work

- Validate gallery-ID-to-coordinate mappings.
- Analyze failed retrieval cases.
- Evaluate additional retrieval and geographic error metrics.
- Explore improvements to cross-view matching and localization robustness.

## Acknowledgements

This project builds on the University-1652 cross-view image retrieval research and its baseline implementation. Please add the appropriate original paper, repository, and dataset citations before public release.

## Disclaimer

This repository documents an experimental baseline. The reported localization performance should not be interpreted as a validated real-world positioning system.
