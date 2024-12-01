document.addEventListener('DOMContentLoaded', () => {
    // Ensure the element exists
    const markdownElement = document.getElementById('markdown-content');
    if (markdownElement) {
        // Import a Markdown parser library (using marked.js in this example)
        const markdownText = markdownElement.textContent;

        // Parse and render the Markdown
        const renderedHTML = marked.parse(markdownText);

        // Replace the original content with the rendered HTML
        markdownElement.innerHTML = renderedHTML;
    }
});
