/** Detect supported fruit objects in the browser and return tight image crops for ResNet50. */
import type { DetectedObject, ObjectDetection } from "@tensorflow-models/coco-ssd";

export type FruitName = "Apel" | "Pisang" | "Jeruk";

export type FruitRegion = {
  fruit: FruitName;
  file: File;
};

const FRUIT_BY_CLASS: Record<string, FruitName> = {
  apple: "Apel",
  banana: "Pisang",
  orange: "Jeruk",
};
const MIN_DETECTION_SCORE = 0.5;
const MAX_DETECTIONS = 24;
const MAX_FRUIT_OBJECTS = 4;
const MAX_CROP_EDGE = 512;

let detectorPromise: Promise<ObjectDetection> | null = null;

function loadDetector(): Promise<ObjectDetection> {
  if (!detectorPromise) {
    detectorPromise = (async () => {
      const tf = await import("@tensorflow/tfjs-core");
      // COCO-SSD uses CPU kernels for some operations even when inference runs on WebGL.
      await import("@tensorflow/tfjs-backend-cpu");
      try {
        await import("@tensorflow/tfjs-backend-webgl");
        if (!(await tf.setBackend("webgl"))) throw new Error("WebGL backend unavailable");
      } catch {
        await import("@tensorflow/tfjs-backend-cpu");
        if (!(await tf.setBackend("cpu"))) {
          throw new Error("Browser tidak mendukung backend deteksi buah.");
        }
      }
      await tf.ready();
      const cocoSsd = await import("@tensorflow-models/coco-ssd");
      return cocoSsd.load({ base: "lite_mobilenet_v2" });
    })().catch((error: unknown) => {
      detectorPromise = null;
      throw error;
    });
  }
  return detectorPromise;
}

function loadImage(file: File): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    const imageUrl = URL.createObjectURL(file);
    image.onload = () => {
      URL.revokeObjectURL(imageUrl);
      resolve(image);
    };
    image.onerror = () => {
      URL.revokeObjectURL(imageUrl);
      reject(new Error("Foto tidak bisa dibaca untuk deteksi buah."));
    };
    image.src = imageUrl;
  });
}

function cropToFile(
  image: HTMLImageElement,
  bbox: [number, number, number, number],
  index: number,
  fruit: FruitName,
): Promise<File> {
  const [boxX, boxY, boxWidth, boxHeight] = bbox;
  const paddingX = boxWidth * 0.08;
  const paddingY = boxHeight * 0.08;
  const left = Math.max(0, boxX - paddingX);
  const top = Math.max(0, boxY - paddingY);
  const right = Math.min(image.naturalWidth, boxX + boxWidth + paddingX);
  const bottom = Math.min(image.naturalHeight, boxY + boxHeight + paddingY);
  const cropWidth = Math.max(1, right - left);
  const cropHeight = Math.max(1, bottom - top);
  const scale = Math.min(1, MAX_CROP_EDGE / Math.max(cropWidth, cropHeight));
  const canvas = document.createElement("canvas");
  canvas.width = Math.max(1, Math.round(cropWidth * scale));
  canvas.height = Math.max(1, Math.round(cropHeight * scale));

  const context = canvas.getContext("2d");
  if (!context) return Promise.reject(new Error("Foto gagal disiapkan untuk ResNet50."));
  context.drawImage(image, left, top, cropWidth, cropHeight, 0, 0, canvas.width, canvas.height);

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => {
        if (!blob) {
          reject(new Error("Potongan foto buah gagal dibuat."));
          return;
        }
        resolve(new File([blob], `buah-${fruit.toLowerCase()}-${index + 1}.jpg`, { type: "image/jpeg" }));
      },
      "image/jpeg",
      0.84,
    );
  });
}

function getRegionBoxes(detection: DetectedObject): Array<[number, number, number, number]> {
  const [x, y, width, height] = detection.bbox;
  if (detection.class !== "banana") return [detection.bbox];

  // A banana bunch can contain fresh and rotten pieces, so inspect overlapping slices.
  if (width >= height) {
    const sliceWidth = width * 0.48;
    return ([0, 0.26, 0.52] as const).map(
      (offset): [number, number, number, number] => [x + width * offset, y, sliceWidth, height],
    );
  }

  const sliceHeight = height * 0.48;
  return ([0, 0.26, 0.52] as const).map(
    (offset): [number, number, number, number] => [x, y + height * offset, width, sliceHeight],
  );
}

/** Detect target fruits and crop each detected object for ResNet50. */
export async function detectFruitRegions(file: File): Promise<FruitRegion[]> {
  const [detector, image] = await Promise.all([loadDetector(), loadImage(file)]);
  const detections = await detector.detect(image, MAX_DETECTIONS, MIN_DETECTION_SCORE);
  const fruitDetections = detections
    .reduce<Array<{ detection: DetectedObject; fruit: FruitName }>>((regions, detection) => {
      const fruit = FRUIT_BY_CLASS[detection.class];
      if (fruit) regions.push({ detection, fruit });
      return regions;
    }, [])
    .sort((left, right) => right.detection.score - left.detection.score);

  if (fruitDetections.length > MAX_FRUIT_OBJECTS) {
    throw new Error("Foto memuat banyak buah. Ambil satu buah lebih dekat agar semua bagian terbaca.");
  }

  const regions = fruitDetections.flatMap((detection) =>
    getRegionBoxes(detection.detection).map((bbox) => ({ fruit: detection.fruit, bbox })),
  );

  return Promise.all(
    regions.map(async (region, index) => ({
      fruit: region.fruit,
      file: await cropToFile(image, region.bbox, index, region.fruit),
    })),
  );
}
