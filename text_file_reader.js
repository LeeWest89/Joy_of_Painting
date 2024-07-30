// Functions to make txt file into a csv file sorted by date
const fs = require('fs');
const path = require('path');

// Read the text file
fs.readFile('Episode_Dates.txt', 'utf8', (error, data) => {
  if (error) {
    console.error('Error reading the file:', error);
    return;
  }
  
  const episodes = parseEpisodes(data);
  const sortedEpisodes = sortEpisodes(episodes);
  writeCSV(sortedEpisodes, 'csv/Episode_Dates.csv');
});

// parses the file content
function parseEpisodes(data) {
  const lines = data.trim().split('\n');
  const episodes = [];
  lines.forEach(line => {
    // Extract date
    const match = line.match(/\((.*?)\)/);
    if (match) {
      const date = new Date(match[1].trim());
      const title = line.split('(')[0].trim();
      const month = date.toLocaleString('default', { month: 'long' });
      const day = date.getDate();
      const year = date.getFullYear();
      episodes.push({ title, month, day, year });
    }
  });
  return (episodes);
}

// sorts episodes by date
function sortEpisodes(episodes) {
  return (episodes.sort((a, b) => {
    const dateA = new Date(`${a.month} ${a.day}, ${a.year}`);
    const dateB = new Date(`${b.month} ${b.day}, ${b.year}`);
    return (dateA - dateB);
  }));
}

// writes data to csv file
function writeCSV(episodes, fileName) {
  const header = 'Episode_TITLE,Month,Day,Year\n';
  const rows = episodes
    .map(({ title, month, day, year }) => `${title},"${month}",${day},${year}`)
    .join('\n');
  const csvContent = header + rows;

  fs.writeFile(path.join(__dirname, fileName), csvContent, 'utf8', error => {
    if (error) {
      console.error('Error writing the csv file:', error);
    } else {
      console.log('csv file has been saved!');
    }
  });
}
