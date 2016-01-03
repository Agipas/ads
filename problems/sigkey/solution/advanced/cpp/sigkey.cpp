#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_set>

typedef std::string key;
typedef unsigned int keymask;

std::vector<key> readInput(std::string fileName) {
    std::ifstream inputFile(fileName, std::ifstream::in);
    
    int keyCount;
    inputFile >> keyCount;
    
    std::vector<key> keys(keyCount);
    for (int i = 0; i < keyCount; i++) {
        key line;
        inputFile >> line;
        keys.at(i) = line;
    }
    
    inputFile.close();
    return keys;
}

int solve(std::vector<key> keys) {
    // For each key, we'll generate two 32-bit masks, where the bits represent the letters in the key.
    // For example, 'acef' corresponds to 0..0000110101 (the rightmost bit is 'a').
    // The second mask is the same but with all greater bits set to 1: 'acef' = 1..1111110101.
    //
    // We'll store both masks for each key in a hashtable.
    // Therefore, if two keys produce a pair, there is a pair of masks in the hashtable
    // whose bitwise AND operation produces all zeroes: 0..0000000000.
    //
    // This way, we can iterate over all positive masks (starting with zeroes),
    // and for each positive mask we'll look up its bitwise inverse in the hashtable.
    //
    // Example:
    //   'acef' and 'bd' produce a key pair.
    //   'acef' gives us two masks: 0..0000110101 and 1..1111110101.
    //     'bd' gives us two masks: 0..0000001010 and 1..1111111010.
    //
    //   For the mask 0..0000001010 there is a matching inverse mask 1..1111110101, so it's a key pair.

    std::unordered_set<keymask> positiveKeyMasks(keys.size());
    std::unordered_set<keymask> negativeKeyMasks(keys.size());
    
    for (key k: keys) {
        keymask positiveMask = 0;
        int mostSignificantBit = 0;
        
        for (int i = 0; i < k.length(); i++) {
            int bitIndex = k[i] - 'a';
            positiveMask |= (1 << bitIndex);
            
            if (bitIndex > mostSignificantBit) {
                mostSignificantBit = bitIndex;
            }
        }

        int negativeMask = ~positiveMask ^ ((1 << mostSignificantBit) - 1) | positiveMask;
        positiveKeyMasks.insert(positiveMask);
        negativeKeyMasks.insert(negativeMask);
    }
    
    int pairCount = 0;
    for (keymask mask: positiveKeyMasks) {
        if (negativeKeyMasks.find(~mask) != negativeKeyMasks.end()) {
            pairCount++;
        }
    }
    
    return pairCount;
}

void writeOutput(std::string fileName, int pairCount) {
    std::ofstream outputFile(fileName, std::ifstream::out);
    outputFile << pairCount;
    outputFile.close();
}

int main(int argc, const char * argv[]) {
    auto keys = readInput("sigkey.in");
    auto pairCount = solve(keys);
    writeOutput("sigkey.out", pairCount);
    return 0;
}
