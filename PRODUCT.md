# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

React, Vite, TypeScript, TensorFlow.js with COCO-SSD Lite for browser fruit detection, FastAPI and TensorFlow/Keras with ResNet50 for freshness classification, and Vercel Services for deployment.

## Users

Primary user: a person testing one photo of an apple, banana, or orange in the UAS fruit-classification demo. The UAS evaluator is an additional inferred audience.

## Product Purpose

Let a visitor upload a fruit photo, detect supported fruit objects, and see the ResNet50 prediction as **Segar** or **Busuk**. When multiple fruit regions are detected, any region predicted **Busuk** makes the overall result **Busuk**.

## Positioning

The website uses COCO-SSD Lite in the browser to detect apple, banana, or orange objects, then serves each detected crop to the fixed ResNet50 training artifact. A region-level six-class argmax is aggregated conservatively: any Busuk region makes the result Busuk. The result is a visual estimate, not a guarantee about food safety or the fruit's interior.

## Operating Context

The product is a small UAS demo. A visitor submits one image at a time from a phone or computer. The application has no account, history, or saved uploads. The intended deployment host is Vercel.

## Capabilities and Constraints

- The only supported fruit classes are fresh and rotten apples, bananas, and oranges.
- Photos with no detected target fruit receive an unsupported result before the ResNet50 API is called. COCO-SSD is a general detector, so this is not a guarantee that every non-fruit photo is rejected.
- Mixed-photo aggregation applies when COCO-SSD returns separate fruit regions. If a bunch is detected as one large region or visible rot is not localized, ResNet50 can still miss it.
- The selected model is `ResNet50_terbaik.keras`, input size 160 × 160 RGB, TensorFlow 2.21.0, with ImageNet ResNet50 preprocessing.
- The model's test report records 97.69% accuracy across 2,727 test images and 31 rotten images predicted into a fresh class (10 apples and 21 oranges). These are evidence from the selected notebook run, not a safety guarantee for new photos.
- The web app accepts one JPEG, PNG, or WebP image at a time, with a 4 MB limit. Uploaded images are processed in memory and are not persisted.
- Inferred for the demo: Indonesian interface copy and a contemporary fruit-market visual context.

## Evidence on Hand

- [Training notebook](https://colab.research.google.com/drive/16t9E0vxdy2ZF-86ZbjetxU_yVwtDOmON?usp=sharing)
- Local model-run evidence: `UAS_AI/buah_cepat_resume_daf3a93e2d/` (configuration, class labels, model metadata, and evaluation report).
- Repository plan: `PLAN.md`.
