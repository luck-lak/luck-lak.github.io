# AOKUN's Portfolio Website

## About

This is the personal portfolio website of Aokun Lei.

The website is currently built with simple HTML, CSS, and JavaScript.

## Project Structure

- `index.html` — Main webpage content
- `learning-records.html` — Learning records navigation page
- `records/` — One standalone page per course or paper note
- `css/` — Website styles
- `js/` — JavaScript and interactions
- `assets/images/` — Personal images and favicon
- `assets/records/` — Course screenshots (`<record-name>/01.jpg`) and navigation covers (`thumbnails/01.jpg`)
- `学习探索记录.docx` — Original complete learning notebook

## Future Updates / Maintenance

The current structure is intentionally simple and easy to maintain.

### Adding New Content

For small updates, such as adding a new section or changing text:

1. Edit `index.html`.
2. Add corresponding styles in `css/style.css` if needed.
3. Add JavaScript in `js/main.js` only when interaction is required.

When adding a new section, keep the structure consistent:

```html
<section class="section-name">
    <h2>Section Title</h2>
    <p>Content...</p>
</section>
```

### Updating Projects

Projects are kept in the `#projects` section of `index.html`. To add one, copy a
`<article class="project-card">` block, then update the project name, GitHub link,
and one-sentence description. The card layout is already defined in
`css/style.css`, so no CSS changes are needed for a normal new project.

```html
<article class="project-card">
    <h3><a href="https://github.com/your-name/your-project">Project Name</a></h3>
    <p>A short description of what the project explores or does.</p>
</article>
```

### Updating Learning Records

The learning records are intentionally kept as plain HTML pages:

1. Create a folder for the detail-page images:
   `assets/records/<record-name>/01.jpg`.
2. Add a navigation cover:
   `assets/records/thumbnails/<record-number>.jpg`.
3. Copy one existing page in `records/`, then update its `<title>`,
   description, kicker, `<h1>`, body content, and image paths.
4. Update the previous/next links at the bottom of the affected record pages.
5. Add a matching card to `learning-records.html`.
6. Keep `学习探索记录.docx` unchanged as the complete archive unless it is
   explicitly being updated.

The current collection is labeled as DeepLearning.AI. When adding Codecademy
or another platform later, keep the collection label clear and consider
splitting the navigation into sections such as `DeepLearning.AI` and
`Codecademy`.

> Agent note: when converting a new note from `学习探索记录.docx`, copy an
> existing record as the template, preserve the user's wording and screenshot
> order, use only plain HTML/CSS relative paths, and update pagination and the
> navigation card. Do not regenerate or rewrite the whole DOCX unless the user
> explicitly asks for that.
