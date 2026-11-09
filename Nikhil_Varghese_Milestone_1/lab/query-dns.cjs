const { Resolver } = require('node:dns').promises;

async function main() {
  const resolver = new Resolver({ timeout: 1500, tries: 1 });
  const server = '127.0.0.1:15353';
  const name = 'orders.test.';
  resolver.setServers([server]);
  console.log(`DNS server ${server} | query ${name} IN A`);
  for (const { address, ttl } of await resolver.resolve4(name, { ttl: true })) {
    console.log(`${name} ${ttl} IN A ${address}`);
  }
}

main().catch((error) => {
  console.error(`DNS query failed: ${error.code ?? error.message}`);
  process.exitCode = 1;
});
