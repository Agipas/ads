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
        Set<String> keySet = new HashSet<>(inputData.getKeys().length);
        for (String key: inputData.getKeys()) {
            char[] keyChars = key.toCharArray();
            Arrays.sort(keyChars);
            String normalizedKey = String.valueOf(keyChars);
            keySet.add(normalizedKey);
        }

        int pairCount = 0;
        for (String publicKey: keySet) {
            if (keySet.contains(getPrivateKey(publicKey))) {
                pairCount++;
            }
        }

        return new SigkeyOutputData(pairCount);
    }

    private static String getPrivateKey(String publicKey) {
        char lastPublicKeyChar = publicKey.charAt(publicKey.length() - 1);
        char[] privateKeyChars = new char[lastPublicKeyChar - 'a' + 1 - publicKey.length()];

        int publicKeyReadPos = 0;
        int privateKeyWritePos = 0;

        for (char alphabetChar = 'a'; alphabetChar < lastPublicKeyChar; alphabetChar++) {
            if (publicKeyReadPos >= publicKey.length()) {
                privateKeyChars[privateKeyWritePos++] = alphabetChar;
                continue;
            }

            while (publicKey.charAt(publicKeyReadPos) < alphabetChar) {
                publicKeyReadPos++;
            }
            if (publicKey.charAt(publicKeyReadPos) != alphabetChar) {
                privateKeyChars[privateKeyWritePos++] = alphabetChar;
            }
            else {
                publicKeyReadPos++;
            }
        }

        return new String(privateKeyChars);
    }

    private static void writeOutput(String outputFileName, SigkeyOutputData outputData) throws IOException {
        try (Writer outputFileWriter = new FileWriter(outputFileName)) {
            outputFileWriter.write(String.valueOf(outputData.getKeyPairCount()));
        }
    }
}
