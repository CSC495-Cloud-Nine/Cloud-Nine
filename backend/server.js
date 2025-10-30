// Minimal registration API server (no external deps)
// POST /api/register
// Stores users in backend/users.json

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const DATA_FILE = path.join(__dirname, 'users.json');

function readUsers(){
  try{ const raw = fs.readFileSync(DATA_FILE, 'utf8'); return JSON.parse(raw || '[]'); }
  catch(e){ return []; }
}

function writeUsers(users){
  fs.writeFileSync(DATA_FILE, JSON.stringify(users, null, 2), 'utf8');
}

function hashPassword(password){
  const salt = crypto.randomBytes(16).toString('hex');
  const derived = crypto.scryptSync(password, salt, 64).toString('hex');
  return { salt, hash: derived };
}

function sendJSON(res, status, obj){
  res.writeHead(status, {'Content-Type':'application/json'});
  res.end(JSON.stringify(obj));
}

const server = http.createServer((req, res)=>{
  if(req.method === 'POST' && req.url === '/api/register'){
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', ()=>{
      try{
        const data = JSON.parse(body || '{}');
        const { firstName, lastName, age, email, password } = data;
        if(!firstName || !lastName || !email || !password){
          return sendJSON(res, 400, { error: 'Missing required fields' });
        }

        const users = readUsers();
        const exists = users.find(u => u.email === email.toLowerCase());
        if(exists) return sendJSON(res, 409, { error: 'Email already registered' });

        const { salt, hash } = hashPassword(password);
        const id = crypto.randomBytes(8).toString('hex');
        const user = { id, firstName, lastName, age, email: email.toLowerCase(), passwordHash: hash, salt, createdAt: new Date().toISOString() };
        users.push(user);
        writeUsers(users);
        sendJSON(res, 201, { message: 'Account created (demo).', id });
      }catch(err){
        console.error('Register error', err);
        sendJSON(res, 500, { error: 'Invalid request or server error' });
      }
    });
    return;
  }

  // Simple CORS and welcome for other requests
  if(req.method === 'OPTIONS'){
    res.writeHead(204, {
      'Access-Control-Allow-Origin':'*',
      'Access-Control-Allow-Methods':'POST,OPTIONS',
      'Access-Control-Allow-Headers':'Content-Type'
    });
    return res.end();
  }

  res.writeHead(200, { 'Content-Type':'application/json', 'Access-Control-Allow-Origin':'*' });
  res.end(JSON.stringify({ status: 'Cloud9 backend demo. Use POST /api/register' }));
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, ()=> console.log(`Cloud9 demo backend listening on http://localhost:${PORT}`));
