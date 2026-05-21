document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generate-form');
    const topicInput = document.getElementById('topic-input');
    const generateBtn = document.getElementById('generate-btn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    const resultSection = document.getElementById('result-section');
    
    const resultImage = document.getElementById('result-image');
    const finalRating = document.getElementById('final-rating');
    const promptText = document.getElementById('prompt-text');
    const critiqueText = document.getElementById('critique-text');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const topic = topicInput.value.trim();
        if (!topic) return;

        // Set Loading State
        btnText.textContent = 'Generating... (This takes a minute)';
        loader.classList.remove('hidden');
        generateBtn.disabled = true;
        resultSection.classList.add('hidden');
        
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to generate thumbnail');
            }

            // Update UI with results
            resultImage.src = data.image_url;
            finalRating.textContent = data.final_rating;
            promptText.textContent = data.prompt;
            critiqueText.textContent = data.critique;

            // Show Results
            resultSection.classList.remove('hidden');
            
            // Scroll to results
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            // Reset Button State
            btnText.textContent = 'Generate Thumbnail';
            loader.classList.add('hidden');
            generateBtn.disabled = false;
        }
    });
});
