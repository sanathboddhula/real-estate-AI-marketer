// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Sync shared address with form fields and auto-populate property data
    const sharedAddress = document.getElementById('shared-address');
    const addressField = document.getElementById('address');
    
    if (sharedAddress && addressField) {
        let debounceTimer;
        
        sharedAddress.addEventListener('input', function() {
            addressField.value = this.value;
            
            // Debounce API calls
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                if (this.value.length > 10) {
                    fetchPropertyData(this.value);
                }
            }, 1000);
        });
    }
    
    // Auto-populate property data from Zillow
    async function fetchPropertyData(address) {
        try {
            const response = await fetch('/get-property-data', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({address: address})
            });
            
            const result = await response.json();
            
            if (result.success && result.property_data) {
                const data = result.property_data;
                // Fill shared fields and hidden form fields
                if (data.price && !document.getElementById('shared-price').value) {
                    document.getElementById('shared-price').value = data.price;
                    document.getElementById('price').value = data.price;
                }
                if (data.bedrooms && !document.getElementById('shared-bedrooms').value) {
                    document.getElementById('shared-bedrooms').value = data.bedrooms;
                    document.getElementById('bedrooms').value = data.bedrooms;
                }
                if (data.bathrooms && !document.getElementById('shared-bathrooms').value) {
                    document.getElementById('shared-bathrooms').value = data.bathrooms;
                    document.getElementById('bathrooms').value = data.bathrooms;
                }
            }
        } catch (error) {
            console.log('Property data fetch failed:', error);
        }
    }
    
    // Zillow URL loading function
    window.loadFromZillow = async function() {
        const url = document.getElementById('zillow-url').value;
        if (!url) {
            alert('Please enter a Zillow URL');
            return;
        }
        
        try {
            const response = await fetch('/api/parse-zillow', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({zillow_url: url})
            });
            
            const result = await response.json();
            
            if (result.success && result.property_data) {
                const data = result.property_data;
                
                // Store data globally
                window.loadedPropertyData = data;
                
                // Sync with hidden fields
                document.getElementById('address').value = data.address || '';
                document.getElementById('price').value = data.price || '';
                document.getElementById('bedrooms').value = data.bedrooms || '';
                document.getElementById('bathrooms').value = data.bathrooms || '';
                
                // Store Zillow image URL if available
                if (data.main_image_url && data.image_available) {
                    const imageInput = document.createElement('input');
                    imageInput.type = 'hidden';
                    imageInput.name = 'zillow_image_url';
                    imageInput.id = 'zillow_image_url';
                    imageInput.value = data.main_image_url;
                    document.getElementById('flyer-form').appendChild(imageInput);
                }
                
                // Show loaded data with image indicator
                const displayDiv = document.getElementById('property-data-display');
                const infoDiv = document.getElementById('loaded-property-info');
                
                const imageStatus = data.image_available ? '📸 Property image found' : '🔍 Using stock image';
                
                infoDiv.innerHTML = `
                    <div><strong>🏡 Address:</strong> ${data.address}</div>
                    <div><strong>💰 Price:</strong> $${data.price?.toLocaleString()}</div>
                    <div><strong>🛏️ Bedrooms:</strong> ${data.bedrooms} <strong>🛁 Bathrooms:</strong> ${data.bathrooms}</div>
                    <div><strong>${imageStatus}</strong></div>
                `;
                
                displayDiv.style.display = 'block';
                alert('✅ Property data loaded successfully!');
            } else {
                alert('❌ Error: ' + (result.error || 'Failed to load property data'));
            }
            
        } catch (error) {
            console.error('Error loading Zillow data:', error);
            alert('❌ Connection error. Please try again.');
        }
    }
    

    

    
    // Tab switching function
    window.switchTab = function(tabId) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Remove active class from all nav tabs
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Show selected tab
        const selectedTab = document.getElementById(tabId);
        if (selectedTab) {
            selectedTab.classList.add('active');
        }
        
        // Add active class to clicked nav tab
        event.target.classList.add('active');
    }

    // Form submission handler
    const flyerForm = document.getElementById('flyer-form');
    if (flyerForm) {
        flyerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Check if property data is loaded
            if (!window.loadedPropertyData) {
                alert('Please load property data from Zillow URL first!');
                return;
            }
            
            const formData = new FormData();
            formData.append('address', document.getElementById('address').value);
            formData.append('price', document.getElementById('price').value);
            formData.append('bedrooms', document.getElementById('bedrooms').value);
            formData.append('bathrooms', document.getElementById('bathrooms').value);
            formData.append('template', document.getElementById('template').value);
            formData.append('format', document.getElementById('format').value);
            
            // Add Zillow image URL if available
            const zillowImageUrl = document.getElementById('zillow_image_url')?.value;
            if (zillowImageUrl) {
                formData.append('zillow_image_url', zillowImageUrl);
            }
            
            // Show loading state
            document.getElementById('loading').style.display = 'block';
            document.getElementById('ai-status').style.display = 'block';
            document.getElementById('generate-btn').disabled = true;
            document.getElementById('generate-btn').textContent = '🔄 Generating...';
            document.getElementById('error').style.display = 'none';
            
            try {
                const response = await fetch('/generate-flyer', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('preview-container').innerHTML = 
                        `<img id="flyer-preview" src="${result.image}" alt="Generated Professional Flyer">`;
                    
                    // Show insights
                    displayInsights(result.neighborhood, result.mortgage, result.property_insights);
                    
                    // Store flyer path
                    window.currentFlyerPath = result.flyer_path;
                } else {
                    throw new Error(result.error || 'Failed to generate flyer');
                }
                
            } catch (error) {
                document.getElementById('error').textContent = `❌ ${error.message}`;
                document.getElementById('error').style.display = 'block';
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('ai-status').style.display = 'none';
                document.getElementById('generate-btn').disabled = false;
                document.getElementById('generate-btn').textContent = '✨ Generate Professional Flyer';
            }
        });
    }

    function displayInsights(neighborhood, mortgage, property) {
        const container = document.getElementById('insights-container');
        const neighborhoodInfo = document.getElementById('neighborhood-info');
        const mortgageInfo = document.getElementById('mortgage-info');
        const propertyInfo = document.getElementById('property-info');
        
        if (!container || !neighborhoodInfo || !mortgageInfo) return;
        
        function isDataAvailable(value) {
            return value && value !== 'N/A' && value !== 'Data unavailable' && value !== 'undefined';
        }
        
        // Financial Insights
        let mortgageHTML = `
            <div class="insight-item">💰 Monthly Payment: $${mortgage.monthly_payment.toLocaleString()}</div>
            <div class="insight-item">🏦 Down Payment (20%): $${mortgage.down_payment.toLocaleString()}</div>`;
        
        if (isDataAvailable(property?.annual_taxes)) {
            mortgageHTML += `<div class="insight-item">🏛️ Property Taxes: $${property.annual_taxes}</div>`;
        }
        mortgageHTML += `<div class="insight-item">📈 Interest Rate: ${mortgage.interest_rate}</div>`;
        
        // Market Performance
        let neighborhoodHTML = '';
        if (isDataAvailable(property?.page_views)) {
            neighborhoodHTML += `<div class="insight-item">👀 Page Views: ${property.page_views}</div>`;
        }
        if (isDataAvailable(property?.days_on_market)) {
            neighborhoodHTML += `<div class="insight-item">📅 Days on Market: ${property.days_on_market}</div>`;
        }
        if (isDataAvailable(property?.price_per_sqft)) {
            neighborhoodHTML += `<div class="insight-item">💲 Price per Sq Ft: $${property.price_per_sqft}</div>`;
        }
        if (isDataAvailable(property?.zestimate)) {
            neighborhoodHTML += `<div class="insight-item">📊 Zestimate: $${property.zestimate}</div>`;
        }
        
        // Location Value
        if (propertyInfo) {
            let locationHTML = '';
            if (isDataAvailable(neighborhood.walkability_score)) {
                locationHTML += `<div class="insight-item">🚶 Walkability Score: ${neighborhood.walkability_score}/100</div>`;
            }
            if (isDataAvailable(property?.school_rating)) {
                locationHTML += `<div class="insight-item">🏫 School Rating: ${property.school_rating}/10</div>`;
            }
            if (isDataAvailable(neighborhood.restaurants_nearby)) {
                locationHTML += `<div class="insight-item">🍽️ Restaurants Nearby: ${neighborhood.restaurants_nearby}</div>`;
            }
            if (isDataAvailable(neighborhood.parks_nearby)) {
                locationHTML += `<div class="insight-item">🏞️ Parks Nearby: ${neighborhood.parks_nearby}</div>`;
            }
            propertyInfo.innerHTML = locationHTML;
        }
        
        neighborhoodInfo.innerHTML = neighborhoodHTML;
        mortgageInfo.innerHTML = mortgageHTML;
        
        container.style.display = 'block';
    }

    // Download flyer
    const downloadBtn = document.getElementById('download-btn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            if (window.currentFlyerPath) {
                const filename = window.currentFlyerPath.split('/').pop();
                window.open(`/download-flyer/${filename}`, '_blank');
            }
        });
    }



    // AI Marketing Suite Functions
    async function callAIEndpoint(endpoint, buttonId, resultTitle) {
        const button = document.getElementById(buttonId);
        const originalText = button.textContent;
        
        button.disabled = true;
        button.textContent = '🔄 Generating...';
        
        const addressInput = document.getElementById('shared-address') || document.getElementById('address');
        const data = { address: addressInput.value };
        
        if (!data.address) {
            alert('Please enter a property address first');
            button.disabled = false;
            button.textContent = originalText;
            return;
        }
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                displayAIResults(result, resultTitle);
            } else {
                alert('❌ Error: ' + result.error);
            }
        } catch (error) {
            alert('❌ Connection Error: ' + error.message);
        } finally {
            button.disabled = false;
            button.textContent = originalText;
        }
    }
    
    function displayAIResults(result, title) {
        const aiResultsContent = document.getElementById('ai-results-content');
        const aiResultsDisplay = document.getElementById('ai-results-display');
        
        if (!aiResultsContent || !aiResultsDisplay) return;
        
        let html = `<h5>${title}</h5>`;
        
        if (result.descriptions) {
            html += '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">';
            html += '<h6>📝 Property Descriptions:</h6>';
            for (const [type, desc] of Object.entries(result.descriptions)) {
                html += `<div style="margin: 10px 0; padding: 10px; background: white; border-radius: 5px;">`;
                html += `<strong>${type.toUpperCase()}:</strong><br>`;
                html += `<textarea readonly style="width: 100%; height: 80px; margin-top: 5px; resize: none;">${desc}</textarea>`;
                html += '</div>';
            }
            html += '</div>';
        }
        
        if (result.social_content) {
            html += '<div style="background: #f0f8ff; padding: 15px; border-radius: 8px; margin: 10px 0;">';
            html += '<h6>📱 Social Media Content:</h6>';
            for (const [platform, content] of Object.entries(result.social_content)) {
                html += `<div style="margin: 10px 0; padding: 10px; background: white; border-radius: 5px;">`;
                html += `<strong>${platform.toUpperCase()}:</strong><br>`;
                if (typeof content === 'object') {
                    for (const [key, value] of Object.entries(content)) {
                        html += `<div style="margin: 5px 0;"><em>${key}:</em> ${value}</div>`;
                    }
                } else {
                    html += `<div>${content}</div>`;
                }
                html += '</div>';
            }
            html += '</div>';
        }
        
        if (result.cma_analysis) {
            html += '<div style="background: #f0fff0; padding: 15px; border-radius: 8px; margin: 10px 0;">';
            html += '<h6>📊 CMA Analysis:</h6>';
            html += `<div style="background: white; padding: 10px; border-radius: 5px; margin: 10px 0;">`;
            html += `<textarea readonly style="width: 100%; height: 120px; resize: none;">${result.cma_analysis.analysis}</textarea>`;
            html += '</div>';
            if (result.cma_analysis.metrics) {
                html += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">';
                for (const [key, value] of Object.entries(result.cma_analysis.metrics)) {
                    html += `<div style="background: white; padding: 8px; border-radius: 5px; text-align: center;">`;
                    html += `<strong>${key.replace('_', ' ').toUpperCase()}:</strong><br>${value}`;
                    html += '</div>';
                }
                html += '</div>';
            }
            html += '</div>';
        }
        
        aiResultsContent.innerHTML = html;
        aiResultsDisplay.style.display = 'block';
        
        // Scroll to results
        aiResultsDisplay.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // AI Marketing Suite Event Listeners
    const descriptionsBtn = document.getElementById('descriptions-btn');
    if (descriptionsBtn) {
        descriptionsBtn.addEventListener('click', function() {
            callAIEndpoint('/generate-descriptions', 'descriptions-btn', '📝 Property Descriptions Generated');
        });
    }
    
    const socialContentBtn = document.getElementById('social-content-btn');
    if (socialContentBtn) {
        socialContentBtn.addEventListener('click', function() {
            callAIEndpoint('/generate-social-content', 'social-content-btn', '📱 Social Media Content Generated');
        });
    }
    
    const cmaBtn = document.getElementById('cma-btn');
    if (cmaBtn) {
        cmaBtn.addEventListener('click', function() {
            callAIEndpoint('/generate-cma', 'cma-btn', '📊 CMA Analysis Generated');
        });
    }
    
    const fullAgentBtn = document.getElementById('full-agent-btn');
    if (fullAgentBtn) {
        fullAgentBtn.addEventListener('click', function() {
            callAIEndpoint('/ai-marketing-agent', 'full-agent-btn', '🚀 Complete Marketing Package Generated');
        });
    }
});