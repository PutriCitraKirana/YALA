const fs = require('fs');
const axios = require('axios');
const readline = require('readline');
const { exec } = require('child_process');

const AUTH_FILE = 'auth.txt';
const BANNER_URL = 'https://raw.githubusercontent.com/Aniketcrypto/aniketcrypto/refs/heads/main/yala.json';
const CLAIM_URL = 'https://api-testnet.yala.org/api/points/dailyCollector';
const POINTS_URL = 'https://api-testnet.yala.org/api/points/myPoints?chain=11155111';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Clear screen function
function clearScreen() {
  process.stdout.write('\u001B[2J\u001B[0;0f');
}

// Display banner from remote URL
async function displayBanner() {
  try {
    const response = await axios.get(BANNER_URL);
    console.log(response.data);
  } catch (error) {
    console.log('Welcome to Yala Claim Script!');
  }
}

// Read accounts from file
function readAuthFile() {
  if (!fs.existsSync(AUTH_FILE)) return [];
  const data = fs.readFileSync(AUTH_FILE, 'utf-8');
  return data.trim().split('\n').map(line => {
    const [name, token] = line.split('|');
    return { name, token };
  });
}

// Write new account to file
function writeAuthFile(name, token) {
  fs.appendFileSync(AUTH_FILE, `${name}|${token}\n`);
  console.log(`Account ${name} added successfully!`);
}

// Claim daily points
async function claimDailyPoints(account) {
  try {
    const headers = {
      'Authorization': `Bearer ${account.token}`,
      'Accept': '*/*'
    };

    const response = await axios.post(CLAIM_URL, {}, { headers });
    console.log(`[Success] Daily check-in for ${account.name}.`);

    // Fetch balance and rank
    const pointsResponse = await axios.get(POINTS_URL, { headers });
    const pointsData = pointsResponse.data;

    console.log(`\nBerries Balance: ${pointsData.totalPoints}`);
    console.log(`Rank: ${pointsData.rank}\n`);
  } catch (error) {
    console.log(`[Error] Failed to claim for ${account.name}: ${error.message}`);
  }
}

// Show main menu
function showMenu() {
  console.log('\n1. Add Account');
  console.log('2. Run Once');
  console.log('3. Claim Every 24h');
  console.log('4. Exit');

  rl.question('Select an option: ', async option => {
    clearScreen();

    switch (option) {
      case '1':
        rl.question('Enter account name: ', name => {
          rl.question('Enter auth token: ', token => {
            writeAuthFile(name, token);
            showMenu();
          });
        });
        break;

      case '2':
        const accounts = readAuthFile();
        for (const account of accounts) {
          await claimDailyPoints(account);
        }
        showMenu();
        break;

      case '3':
        console.log('Starting 24-hour scheduler... Press Ctrl+C to stop.');
        setInterval(async () => {
          const accounts = readAuthFile();
          for (const account of accounts) {
            await claimDailyPoints(account);
          }
        }, 24 * 60 * 60 * 1000);
        break;

      case '4':
        console.log('Exiting...');
        rl.close();
        break;

      default:
        console.log('Invalid option. Try again.');
        showMenu();
    }
  });
}

(async function main() {
  clearScreen();
  await displayBanner();
  showMenu();
})();
