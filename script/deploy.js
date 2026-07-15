const hre = require("hardhat");

async function main() {
  // Find the custom flag in the command line arguments
  const flagIndex = process.argv.indexOf("--fadaka-blockchain");
  let network = "default";

  if (flagIndex !== -1 && process.argv[flagIndex + 1]) {
    network = process.argv[flagIndex + 1];
  }

  console.log(`Deploying contracts to the ${network} blockchain...`);

  // Insert your contract deployment logic here
  // const MyContract = await hre.ethers.getContractFactory("YourContractName");
  // const contract = await MyContract.deploy();
  // await contract.waitForDeployment();
  // console.log(`Contract deployed to: ${await contract.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
