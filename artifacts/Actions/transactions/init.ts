import {
  Token,
  Transfer,
  USD,
  TokenAmount
} from '@mimicprotocol/lib-ts'

import { inputs } from './types'
import { ERC20 } from './types/ERC20'

export default function main(): void {

  // ----------------------------------------
  // Token Contract
  // ----------------------------------------

  const tokenContract =
    new ERC20(
      inputs.token,
      inputs.chainId
    )

  // ----------------------------------------
  // Recipient Balance
  // ----------------------------------------

  const balance =
    tokenContract.balanceOf(
      inputs.recipient
    )

  // ----------------------------------------
  // Token Metadata
  // ----------------------------------------

  const token =
    Token.fromAddress(
      inputs.token,
      inputs.chainId
    )

  // ----------------------------------------
  // USD Conversion
  // ----------------------------------------

  const balanceInUsd =
    TokenAmount
      .fromBigInt(token, balance)
      .toUsd()

  const thresholdUsd =
    USD.fromI32(inputs.thresholdUSD)

  console.log(
    'Balance in USD: ' +
    balanceInUsd.toString()
  )

  // ----------------------------------------
  // Threshold Check
  // ----------------------------------------

  if (balanceInUsd.lt(thresholdUsd)) {

    console.log(
      'Threshold below minimum, sending tokens...'
    )

    const transfer =
      Transfer.create(
        inputs.chainId,
        inputs.token,
        inputs.amount,
        inputs.recipient,
        inputs.fee
      )

    console.log(
      'Transfer created successfully'
    )

  } else {

    console.log(
      'Balance is above threshold'
    )
  }
}
