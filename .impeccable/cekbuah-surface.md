# CekBuah surface brief

Operate surface for one photo of an apple, banana, or orange. The visitor chooses a photo, starts one check, and sees the ResNet50 output as **Segar** or **Busuk**, together with the fruit name and the processing steps returned by the backend. The history is local to the current check; photos are not saved. The result is a visual estimate, not a guarantee about the inside of a fruit.

## Direction contract

**THESIS:** Make one fruit photo feel like it has entered a focused inspection light. The result is a clear condition label, supported by the real ResNet50 workflow.

**OWN-WORLD:** Follow the user's supplied Clarid reference: a full-bleed near-black canvas with teal, blue, and violet edge light; one large glass orb with a vertical lavender beam behind a centered editorial serif headline; a restrained pill navigation; violet actions; and a compact, dark three-part specification band. Do not put the whole app inside a floating rounded frame. Use DM Serif Display for large headlines and Manrope for the working interface. Use bright green and red for completed/fresh and error/rotten states.

**STORY:** The first screen introduces the inspection and supported fruit. One CTA moves to the upload; the user chooses one JPEG, PNG, or WebP photo and explicitly starts the check. The page displays the backend's five processing steps, then the model's label. Fast step events play in order and remain visible long enough to read, while each duration remains the backend's measured duration. The process stays usable at phone widths.

**FIRST VIEWPORT:** The page fills the screen with a simple wordmark, a centered navigation pill, and a violet action. A large, centered serif headline sits over a globe-like illuminated image with orbit lines, followed by a short product explanation, the three supported fruit names, and a three-column band containing only real specifications: supported fruit count, 160 × 160 input size, and ResNet50. The upload panel follows directly below the band.

**SIGNATURE MOVE:** A large SVG glass globe carries the hero atmosphere: a lavender vertical beam, thin curved orbit lines, and a few restrained flares. The image stays behind the headline and visually leads down to the violet specification capsule.

**HONEST RISK:** The supplied reference contains invented finance partners and audience metrics. CekBuah replaces those with supported fruit names and actual model details. No audience counts or accuracy percentage appear in this UI.

**FORM:** User-pinned screenshot direction (the user confirmed it should guide the style 100%). The direction seed roll was `seed:e35f4944c29bd4a0`; its assignment does not override the pinned reference. Build code-led and keep existing upload, inference, result, and process-history behavior as the product source of truth.

**FINISH:** Review desktop and 390px mobile captures, inspect the upload and result states, run the design detector once, then document the replacement system in DESIGN.md and `.impeccable/design.json`.
