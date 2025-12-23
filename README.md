Personal site content guide

- Add images into `assets/images/` and videos into `assets/videos/`.
- Use descriptive filenames (e.g., `project-cat-hero.jpg`, `exh-1-1.jpg`).
- To make an exhibition show images, edit the `exhibitionData` object in `1.html` and add an `images` array and/or `videos` array, e.g.: 

  'exh-1': { title: '...', images: ['assets/images/exh-1-1.jpg'], videos: ['assets/videos/exh-1-demo.mp4'], ... }

- To attach media to a project, add `images` / `videos` arrays to the relevant entry in `projectData`.

Notes
- For local video playback, open the page via a local web server (e.g., `python -m http.server`) rather than `file://`, otherwise browsers may block playback.
- I can add an importer script or automatically generate data files from a folder of named assets if you want. Let me know the preferred naming scheme.