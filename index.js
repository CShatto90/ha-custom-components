const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const SCREENSHOTS_DIR = './screenshots';
const API_CALLS_FILE = './api_calls.json';

// Create screenshots directory if it doesn't exist
if (!fs.existsSync(SCREENSHOTS_DIR)) {
  fs.mkdirSync(SCREENSHOTS_DIR);
}

async function monitorTraffic(url, monitorTime = 10000) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Store API calls
  const apiCalls = [];
  
  // Listen for API calls
  page.on('request', request => {
    const url = request.url();
    if (url.includes('recollect.net') || 
        url.includes('collection_schedule') || 
        url.includes('trash_pickup')) {
      console.log(`Request: ${request.method()} ${url}`);
      apiCalls.push({
        type: 'request',
        method: request.method(),
        url: url,
        timestamp: new Date().toISOString()
      });
    }
  });

  page.on('response', async response => {
    const url = response.url();
    if (url.includes('recollect.net') || 
        url.includes('collection_schedule') || 
        url.includes('trash_pickup')) {
      console.log(`Response: ${response.status()} ${url}`);
      try {
        const responseData = await response.json();
        apiCalls.push({
          type: 'response',
          status: response.status(),
          url: url,
          data: responseData,
          timestamp: new Date().toISOString()
        });
      } catch (e) {
        console.log('Could not parse response as JSON:', e.message);
      }
    }
  });

  try {
    // Navigate to the page
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 15000 });
    console.log('Navigation completed. Status:', page.url() !== 'about:blank' ? '200' : 'Failed');
    
    // Take initial screenshot
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'initial.png') });
    
    // Monitor for specified time
    console.log(`Monitoring for ${monitorTime/1000} seconds...`);
    await new Promise(resolve => setTimeout(resolve, monitorTime));
    
    // Take final screenshot
    console.log('Monitoring complete. Taking final screenshot...');
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'final.png') });
    
    // Save API calls to file
    fs.writeFileSync(API_CALLS_FILE, JSON.stringify(apiCalls, null, 2));
    
  } catch (error) {
    console.error('Error during monitoring:', error);
  } finally {
    console.log('Closing browser...');
    await browser.close();
  }
}

// Run the monitor
monitorTraffic('https://www.houstontx.gov/solidwaste/collection-schedule.html'); 