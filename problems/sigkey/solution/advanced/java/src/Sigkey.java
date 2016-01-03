import java.io.*;
import java.util.*;

public class Sigkey {

    public static void main(String[] args) throws IOException {
        String inputFileName = args.length >= 2 ? args[0] : "sigkey.in";
        String outputFileName = args.length >= 2 ? args[1] : "sigkey.out";

        SigkeyInputData inputData = readInput(inputFileName);
        SigkeyOutputData outputData = solve(inputData);
        writeOutput(outputFileName, outputData);
    }

    private static SigkeyInputData readInput(String inputFileName) throws IOException {
        File inputFile = new File(inputFileName);
        try (FileReader inputFileReader = new FileReader(inputFile)) {
            try (BufferedReader bufferedReader = new BufferedReader(inputFileReader)) {
                int keyCount = Integer.valueOf(bufferedReader.readLine());

                String[] keys = new String[keyCount];
                for (int i = 0; i < keyCount; i++) {
                    keys[i] = bufferedReader.readLine();
                }

                return new SigkeyInputData(keys);
            }
        }
    }

    private static SigkeyOutputData solve(SigkeyInputData inputData) {
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

        Set<Integer> positiveKeyMaskSet = new HashSet<>(inputData.getKeys().length);
        Set<Integer> negativeKeyMaskSet = new HashSet<>(inputData.getKeys().length);
        
        for (String key: inputData.getKeys()) {
            int positiveBitMask = 0;
            int mostSignificantBit = 0;
            
            for (int i = 0; i < key.length(); i++) {
                int bitIndex = key.charAt(i) - 'a';
                positiveBitMask |= (1 << bitIndex);

                if (bitIndex > mostSignificantBit) {
                    mostSignificantBit = bitIndex;
                }
            }

            int negativeBitMask = ~positiveBitMask ^ ((1 << mostSignificantBit) - 1) | positiveBitMask;
            positiveKeyMaskSet.add(positiveBitMask);
            negativeKeyMaskSet.add(negativeBitMask);
        }

        int pairCount = 0;
        for (int key: positiveKeyMaskSet) {
            if (negativeKeyMaskSet.contains(~key)) {
                pairCount++;
            }
        }

        return new SigkeyOutputData(pairCount);
    }

    private static void writeOutput(String outputFileName, SigkeyOutputData outputData) throws IOException {
        try (Writer outputFileWriter = new FileWriter(outputFileName)) {
            outputFileWriter.write(String.valueOf(outputData.getKeyPairCount()));
        }
    }
}
