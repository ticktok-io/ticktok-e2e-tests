const ticktok = require('ticktok')

const domain = process.env.TICKTOK_DOMAIN || 'http://localhost:9643'
const token = process.env.TICKTOK_TOKEN || 'ticktok-zY3wpR'

const t = ticktok(domain, token)

t.schedule({ name: 'sanity-30', schedule: 'every.30.seconds' }, () => { console.log(`${new Date().toLocaleString()} tick-30`) })
t.schedule({ name: 'sanity-15', schedule: 'every.15.seconds' }, () => { console.log(`${new Date().toLocaleString()} tick-15`) })
t.schedule({ name: 'sanity-1', schedule: 'every.1.minutes' }, () => { console.log(`${new Date().toLocaleString()} tick-1`) })
setTimeout(() => {
  t.tick({ name: 'sanity-1', schedule: 'every.1.minutes' })
}, 5000)
