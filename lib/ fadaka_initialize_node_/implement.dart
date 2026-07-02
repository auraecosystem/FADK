import 'dart:ffi';
import 'dart:io';
import 'package:ffi/ffi.dart'; // Requires package:ffi for string conversions
import 'fadaka_bindings.g.dart';

void main() {
  // 1. Load the compiled C++ shared object platform binary
  final DynamicLibrary fadakaLib = Platform.isAndroid
      ? DynamicLibrary.open('libfadaka_bft.so')
      : DynamicLibrary.process();

  final bindings = FadakaBindings(fadakaLib);

  // 2. Allocate low-level memory block arena for private/public keys (32 bytes each)
  final Pointer<Uint8> privateKeyBuffer = calloc<Uint8>(32);
  final Pointer<Uint8> publicKeyBuffer = calloc<Uint8>(32);

  try {
    final resultCode = bindings.fadaka_generate_keypair(privateKeyBuffer, publicKeyBuffer);
    
    if (resultCode == 0) {
      print('FADK Keypair initialized successfully via Native FFI.');
    }
  } finally {
    // 3. Always clear manual native allocations out of memory heaps
    calloc.free(privateKeyBuffer);
    calloc.free(publicKeyBuffer);
  }
}
