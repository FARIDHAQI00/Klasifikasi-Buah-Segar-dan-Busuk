# CekBuah surface brief

Operate surface for one photo of an apple, banana, or orange. The visitor chooses a photo, starts one check, and sees the ResNet50 output as **Segar** or **Busuk**, together with the fruit name and the processing steps returned by the backend. The history is local to the current check; photos are not saved. The result is a visual estimate, not a guarantee about the inside of a fruit.

## Direction contract

**THESIS:** Make one fruit photo feel like it has entered a focused inspection light. The result is a clear condition label, supported by the real ResNet50 workflow.

**OWN-WORLD:** Follow the user's supplied Clarid reference: an inset near-black page inside a blue, teal, and violet outer field; one centered luminous orbit behind a large editorial serif headline; a restrained pill navigation; violet actions; and a compact, dark three-part specification band. Use DM Serif Display for large headlines and Manrope for the working interface. Use green and red only for the Segar and Busuk result states.

**STORY:** The first screen introduces the inspection and supported fruit. One CTA moves to the upload; the user chooses one JPEG, PNG, or WebP photo and explicitly starts the check. The page displays the backend's five processing steps, then the model's label. The process stays usable at phone widths.

**FIRST VIEWPORT:** The black inset has a simple wordmark, a centered navigation pill, and a violet action. A two-line, centered serif headline sits over one abstract orbit, followed by a short product explanation, the three supported fruit names, and a three-column band containing only real specifications: supported fruit count, 160 × 160 input size, and ResNet50. The upload panel follows directly below the band.

**SIGNATURE MOVE:** A single CSS-drawn light orbit frames the hero copy and visually leads down to the violet specification capsule. It is geometric interface lighting, not fruit imagery; it does not cover the title or task controls.

**HONEST RISK:** The supplied reference contains invented finance partners and audience metrics. CekBuah replaces those with supported fruit names and actual model details. No audience counts or accuracy percentage appear in this UI.

**FORM:** User-pinned screenshot direction (the user confirmed it should guide the style 100%). The direction seed roll was `seed:e35f4944c29bd4a0`; its assignment does not override the pinned reference. Build code-led and keep existing upload, inference, result, and process-history behavior as the product source of truth.

**FINISH:** Review desktop and 390px mobile captures, inspect the upload and result states, run the design detector once, then document the replacement system in DESIGN.md and `.impeccable/design.json`.
