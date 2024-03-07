const fs = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');

const baseDirectory = '/workspaces/Information-Retrieval-Project/Collected pages';
let folderCounter = 1; // Counter for naming folders

// Function to fetch web page content
async function fetchPage(url) {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error(`Error fetching page: ${error}`);
        return null;
    }
}

// Function to parse HTML content and extract links and content
function parseHTML(html) {
    const $ = cheerio.load(html);
    const links = [];
    const content = $('body').text(); // Extract only text content without HTML tags
    $('a').each((index, element) => {
        const href = $(element).attr('href');
        if (href) {
            // Exclude links to images and videos
            if (!isImage(href) && !isVideo(href)) {
                links.push(href);
            }
        }
    });
    return { links, content };
}

// Function to check if a link is an image
function isImage(link) {
    return /\.(jpg|jpeg|png|gif)$/i.test(link);
}

// Function to check if a link is a video
function isVideo(link) {
    return /\.(mp4|avi|mov|wmv)$/i.test(link);
}

// Function to create folder and files for data and links
function createFolderAndFiles() {
    const folderName = `fol${folderCounter++}`;
    const folderPath = path.join(baseDirectory, folderName);
    fs.mkdirSync(folderPath, { recursive: true });
    fs.writeFileSync(path.join(folderPath, 'data.txt'), '', 'utf-8');
    fs.writeFileSync(path.join(folderPath, 'links.txt'), '', 'utf-8');
    return folderPath;
}

// Function to crawl a webpage and its links recursively
async function crawl(url, depth, visited = new Set()) {
    if (depth === 0 || visited.has(url)) {
        return;
    }
    console.log(`Crawling: ${url}`);
    visited.add(url);
    
    const html = await fetchPage(url);
    if (!html) {
        return;
    }
    
    const { links, content } = parseHTML(html);
    const folderPath = createFolderAndFiles();
    
    // Save content to data.txt
    fs.writeFileSync(path.join(folderPath, 'data.txt'), content, 'utf-8'); // Save only the text content
    
    // Save links to links.txt
    fs.writeFileSync(path.join(folderPath, 'links.txt'), url, 'utf-8');
    
    for (const link of links) {
        await crawl(link, depth - 1, visited);
    }
}

// Array of starting URLs
const startingUrls = [
    'https://www.cricbuzz.com/cricket-news'
];

// Depth to crawl
const depth = 10;

// Start crawling for each starting URL
for (const startingUrl of startingUrls) {
    crawl(startingUrl, depth);
}
