// const fs = require('fs');
// const path = require('path');

// // Read the content of the text file
// fs.readFile('Episode_Dates.txt', 'utf8', (err, data) => {
//   if (err) {
//     console.error('Error reading the file:', err);
//     return;
//   }
  
//   const episodes = parseEpisodes(data);
//   const sortedEpisodes = sortEpisodes(episodes);
//   writeCSV(sortedEpisodes, 'Episode_Dates.csv');
// });

// // Function to parse the file content into a dictionary
// function parseEpisodes(data) {
//   const lines = data.trim().split('\n');
//   const episodes = [];
//   lines.forEach(line => {
//     // Extract date between the first pair of parentheses
//     const match = line.match(/\((.*?)\)/);
//     if (match) {
//       const date = match[1].trim();
//       // Assuming the title is everything before the first parenthesis
//       const title = line.split('(')[0].trim();
//       episodes.push({ title, date });
//     }
//   });
//   return episodes;
// }

// // Function to sort episodes by date
// function sortEpisodes(episodes) {
//   return episodes.sort((a, b) => {
//     const dateA = new Date(a.date);
//     const dateB = new Date(b.date);
//     return dateA - dateB;
//   });
// }

// // Function to write data to a CSV file
// function writeCSV(episodes, fileName) {
//   const header = 'Episode_TITLE,DATE\n';
//   const rows = episodes
//     .map(({ title, date }) => `${title},"${date}"`)
//     .join('\n');
//   const csvContent = header + rows;

//   fs.writeFile(path.join(__dirname, fileName), csvContent, 'utf8', err => {
//     if (err) {
//       console.error('Error writing the CSV file:', err);
//     } else {
//       console.log('CSV file has been saved!');
//     }
//   });
// }

const fs = require('fs');
const path = require('path');

// Read the content of the text file
fs.readFile('Episode_Dates.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the file:', err);
    return;
  }
  
  const episodes = parseEpisodes(data);
  const sortedEpisodes = sortEpisodes(episodes);
  writeCSV(sortedEpisodes, 'Episode_Dates.csv');
});

// Function to parse the file content into an array of objects
function parseEpisodes(data) {
  const lines = data.trim().split('\n');
  const episodes = [];
  lines.forEach(line => {
    // Extract date between the first pair of parentheses
    const match = line.match(/\((.*?)\)/);
    if (match) {
      const date = new Date(match[1].trim());
      // Assuming the title is everything before the first parenthesis
      const title = line.split('(')[0].trim();
      const month = date.toLocaleString('default', { month: 'long' });
      const day = date.getDate();
      const year = date.getFullYear();
      episodes.push({ title, month, day, year });
    }
  });
  return episodes;
}

// Function to sort episodes by date
function sortEpisodes(episodes) {
  return episodes.sort((a, b) => {
    const dateA = new Date(`${a.month} ${a.day}, ${a.year}`);
    const dateB = new Date(`${b.month} ${b.day}, ${b.year}`);
    return dateA - dateB;
  });
}

// Function to write data to a CSV file
function writeCSV(episodes, fileName) {
  const header = 'Episode_TITLE,Month,Day,Year\n';
  const rows = episodes
    .map(({ title, month, day, year }) => `${title},"${month}",${day},${year}`)
    .join('\n');
  const csvContent = header + rows;

  fs.writeFile(path.join(__dirname, fileName), csvContent, 'utf8', err => {
    if (err) {
      console.error('Error writing the CSV file:', err);
    } else {
      console.log('CSV file has been saved!');
    }
  });
}
