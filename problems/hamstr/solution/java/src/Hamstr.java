import java.io.*;
import java.util.Scanner;

public class Hamstr {

    public static void main(String[] args) throws IOException {
        String inputFileName = args.length >= 2 ? args[0] : "hamstr.in";
        String outputFileName = args.length >= 2 ? args[1] : "hamstr.out";

        HamstrInputData inputData = readInput(inputFileName);
        HamstrOutputData outputData = solve(inputData);
        writeOutput(outputFileName, outputData);
    }

    private static HamstrInputData readInput(String inputFileName) throws FileNotFoundException {
        File inputFile = new File(inputFileName);

        try (Scanner inputFileScanner = new Scanner(inputFile)) {
            long dailyBudget = Long.parseLong(inputFileScanner.nextLine());
            int hamsterCount = Integer.parseInt(inputFileScanner.nextLine());

            Hamster[] hamsters = new Hamster[hamsterCount];
            for (int i = 0; i < hamsterCount; i++) {
                String[] hamsterParams = inputFileScanner.nextLine().split(" ");
                int hunger = Integer.parseInt(hamsterParams[0]);
                int greed = Integer.parseInt(hamsterParams[1]);
                hamsters[i] = new Hamster(hunger, greed);
            }

            return new HamstrInputData(dailyBudget, hamsters);
        }
    }

    private static HamstrOutputData solve(HamstrInputData inputData) {
        // Checking if it's possible for us to buy exactly 'candidateHamsterCount' hamsters.
        // Since 'candidateHamsterCount' is a sorted sequence from 0 to C, we can use binary search
        // instead of linear search to locate the optimal count faster.
        int left = 0;
        int right = inputData.getHamsters().length;

        while (left < right) {
            int candidateHamsterCount = (left + right + 1) / 2;
            if (!canBuyKHamsters(candidateHamsterCount, inputData.getHamsters(), inputData.getDailyBudget())) {
                right = candidateHamsterCount - 1;
            }
            else {
                left = candidateHamsterCount;
            }
        }

        int maxAffordableHamsterCount = right;
        return new HamstrOutputData(maxAffordableHamsterCount);
    }

    private static boolean canBuyKHamsters(int k, Hamster[] hamsters, long dailyBudget) {
        long[] hamsterDailyNeeds = new long[hamsters.length];
        for (int i = 0; i < hamsters.length; i++) {
            hamsterDailyNeeds[i] = hamsters[i].getDailyFoodNeeds(k - 1);
        }

        long requiredBudgetForBestKHamsters = 0;
        MergeSort.sort(hamsterDailyNeeds);
        for (int i = 0; i < k; i++) {
            requiredBudgetForBestKHamsters += hamsterDailyNeeds[i];
        }

        return requiredBudgetForBestKHamsters <= dailyBudget;
    }

    private static void writeOutput(String outputFileName, HamstrOutputData outputData) throws IOException {
        try (Writer outputFileWriter = new FileWriter(outputFileName)) {
            outputFileWriter.write(String.valueOf(outputData.getMaxAffordableHamsters()));
        }
    }
}
