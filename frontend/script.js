// Chat functionality
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');

// Auto-resize textarea
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Send message on Enter (Shift+Enter for new line)
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Set message from quick action buttons
function setMessage(text) {
    userInput.value = text;
    userInput.focus();
}

// Send message function
async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');

    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';

    // Disable send button
    setLoading(true);

    try {
        // Call API - use relative URL so it works on any deployment
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Handle different response types
        if (data.type === 'analysis') {
            // Full property analysis
            displayPropertyAnalysis(data);
        } else if (data.type === 'conversation' || data.type === 'chat') {
            // General conversation
            addMessage(data.message, 'assistant');
        } else if (data.type === 'error') {
            // Error message
            addMessage(`Error: ${data.message}`, 'assistant');
        }

    } catch (error) {
        console.error('Error:', error);
        addMessage(`Error: ${error.message}. Make sure the server is running.`, 'assistant');
    } finally {
        setLoading(false);
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = text.replace(/\n/g, '<br>');

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Display full property analysis
function displayPropertyAnalysis(data) {
    const { property_data, deal_analysis, repair_estimate, ai_analysis, address } = data;

    // Create property card HTML
    const propertyCard = `
        <div class="property-card">
            <h3>📍 ${property_data.address || address}</h3>

            <div class="property-details">
                <div class="detail-item">
                    <strong>Price</strong>
                    $${property_data.price?.toLocaleString() || 'N/A'}
                </div>
                <div class="detail-item">
                    <strong>Bedrooms</strong>
                    ${property_data.bedrooms || 'N/A'} beds
                </div>
                <div class="detail-item">
                    <strong>Bathrooms</strong>
                    ${property_data.bathrooms || 'N/A'} baths
                </div>
                <div class="detail-item">
                    <strong>Square Feet</strong>
                    ${property_data.sqft?.toLocaleString() || 'N/A'} sqft
                </div>
                <div class="detail-item">
                    <strong>Year Built</strong>
                    ${property_data.year_built || 'N/A'}
                </div>
                <div class="detail-item">
                    <strong>Property Type</strong>
                    ${property_data.property_type || 'N/A'}
                </div>
            </div>

            <hr style="margin: 15px 0; border: none; border-top: 1px solid #e2e8f0;">

            <h3 style="color: #e7e9ea; margin-top: 15px;">Investment Metrics</h3>

            <div class="property-details">
                <div class="detail-item">
                    <strong>ARV (After Repair Value)</strong>
                    $${deal_analysis.arv?.toLocaleString() || 'N/A'}
                </div>
                <div class="detail-item">
                    <strong>Estimated Repairs (${repair_estimate.repair_level})</strong>
                    $${deal_analysis.estimated_repairs?.toLocaleString() || 'N/A'}
                </div>
                <div class="detail-item">
                    <strong>Max Allowable Offer</strong>
                    $${deal_analysis.max_allowable_offer?.toLocaleString() || 'N/A'}
                </div>
                <div class="detail-item">
                    <strong>Potential Profit</strong>
                    $${deal_analysis.potential_profit?.toLocaleString() || 'N/A'}
                </div>
                <div class="detail-item">
                    <strong>ROI</strong>
                    ${deal_analysis.roi_percentage?.toFixed(2) || 'N/A'}%
                </div>
                <div class="detail-item">
                    <strong>Total Investment</strong>
                    $${deal_analysis.total_investment?.toLocaleString() || 'N/A'}
                </div>
            </div>

            <div style="margin-top: 15px;">
                <span class="deal-rating ${deal_analysis.deal_rating}">
                    ${deal_analysis.deal_rating} DEAL
                </span>
            </div>

            <div class="analysis-section">
                <strong style="color: #e7e9ea; font-size: 15px;">Analysis:</strong><br><br>${ai_analysis}
            </div>
        </div>
    `;

    // Add to chat
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.style.maxWidth = '95%';
    contentDiv.innerHTML = propertyCard;

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Set loading state
function setLoading(isLoading) {
    sendBtn.disabled = isLoading;

    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}
