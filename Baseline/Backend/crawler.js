const fs = require('fs').promises;
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');
const { URL } = require('url'); // for URL validation

const baseDirectory = '/workspaces/Information-Retrieval-Project/CollectedPages';
let folderCounter = 1; // Counter for naming folders

async function fetchPage(url) {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error(`Error fetching page: ${error.message}`);
        return null;
    }
}

function parseHTML(html) {
    const $ = cheerio.load(html);
    const links = [];
    const content = $('body').text(); // Extract only text content without HTML tags
    $('a').each((index, element) => {
        const href = $(element).attr('href');
        if (href) {
            try {
                const absoluteUrl = new URL(href, url).toString(); // Normalize URL
                if (!isImage(absoluteUrl) && !isVideo(absoluteUrl)) {
                    links.push(absoluteUrl);
                }
            } catch (error) {
                console.error(`Invalid URL: ${href}`);
            }
        }
    });
    return { links, content };
}

function isImage(link) {
    return /\.(jpg|jpeg|png|gif)$/i.test(link);
}

function isVideo(link) {
    return /\.(mp4|avi|mov|wmv)$/i.test(link);
}

async function createFolderAndFiles() {
    const folderName = `folder${folderCounter++}`;
    const folderPath = path.join(baseDirectory, folderName);
    await fs.mkdir(folderPath, { recursive: true });
    await fs.writeFile(path.join(folderPath, 'data.txt'), '', 'utf-8');
    await fs.writeFile(path.join(folderPath, 'links.txt'), '', 'utf-8');
    return folderPath;
}

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
    const folderPath = await createFolderAndFiles();
    
    try {
        await fs.writeFile(path.join(folderPath, 'data.txt'), content, 'utf-8');
        await fs.appendFile(path.join(folderPath, 'links.txt'), `${url}\n`, 'utf-8');
    } catch (error) {
        console.error(`Error writing file: ${error.message}`);
    }

    for (const link of links) {
        await crawl(link, depth - 1, visited);
    }
}

const startingUrls = [
    'https://www.cricbuzz.com/cricket-news'
];

const depth = 10;

for (const startingUrl of startingUrls) {
    crawl(startingUrl, depth);
}

