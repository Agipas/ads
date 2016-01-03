import java.io.*;
import java.math.BigInteger;
import java.util.Scanner;

public class Bugtrk {

    public static void main(String[] args) throws IOException {
        String inputFileName = args.length >= 2 ? args[0] : "bugtrk.in";
        String outputFileName = args.length >= 2 ? args[1] : "bugtrk.out";

        BugtrkInputData inputData = readInput(inputFileName);
        BugtrkOutputData outputData = solve(inputData);
        writeOutput(outputFileName, outputData);
    }

    private static BugtrkInputData readInput(String inputFileName) throws FileNotFoundException {
        File inputFile = new File(inputFileName);

        try (Scanner inputFileScanner = new Scanner(inputFile)) {
            long bugCount = inputFileScanner.nextLong();
            long sheetWidth = inputFileScanner.nextLong();
            long sheetHeight = inputFileScanner.nextLong();

            return new BugtrkInputData(bugCount, sheetWidth, sheetHeight);
        }
    }

    private static BugtrkOutputData solve(BugtrkInputData inputData) {
        // Checking if it's possible to fit everything on a board of size exactly 'candidateBoardSize'.
        // Since 'candidateBoardSize' is a sorted sequence from 1 to [some large number],
        // we can use binary search instead of linear search to locate the optimal size faster.
        BigInteger left = BigInteger.ONE;
        BigInteger right = BigInteger.valueOf(inputData.getBugCount() * (Math.max(inputData.getSheetWidth(), inputData.getSheetHeight())));

        // Since we're interested in the minimum size (not just arbitrary suitable size),
        // we need to find the leftmost item among the suitable ones.
        // Comparisons and boundary arithmetics are very important here.
        while (right.subtract(left).compareTo(BigInteger.ONE) > 0) {
            BigInteger candidateBoardSize = left.add(right.subtract(left).divide(BigInteger.valueOf(2)));
            if (canFitEverythingIntoBoardSize(candidateBoardSize, inputData.getBugCount(), inputData.getSheetWidth(), inputData.getSheetHeight())) {
                right = candidateBoardSize;
            }
            else {
                left = candidateBoardSize;
            }
        }

        BigInteger minAcceptableBoardSize = right;
        return new BugtrkOutputData(minAcceptableBoardSize.longValue());
    }

    private static boolean canFitEverythingIntoBoardSize(BigInteger boardSize, long bugCount, long sheetWidth, long sheetHeight) {
        BigInteger cardsPerRow = boardSize.divide(BigInteger.valueOf(sheetWidth));
        BigInteger cardsPerColumn = boardSize.divide(BigInteger.valueOf(sheetHeight));
        return cardsPerRow.multiply(cardsPerColumn).compareTo(BigInteger.valueOf(bugCount)) >= 0;
    }

    private static void writeOutput(String outputFileName, BugtrkOutputData outputData) throws IOException {
        try (Writer outputFileWriter = new FileWriter(outputFileName)) {
            outputFileWriter.write(String.valueOf(outputData.getMaxBoardSize()));
        }
    }
}
