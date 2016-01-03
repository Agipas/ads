import java.io.*;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Scanner;

public class Discnt {

    public static void main(String[] args) throws IOException {
        String inputFileName = args.length >= 2 ? args[0] : "discnt.in";
        String outputFileName = args.length >= 2 ? args[1] : "discnt.out";

        DiscntInputData inputData = readInput(inputFileName);
        DiscntOutputData outputData = solve(inputData);
        writeOutput(outputFileName, outputData);
    }

    private static DiscntInputData readInput(String inputFileName) throws FileNotFoundException {
        File inputFile = new File(inputFileName);

        try (Scanner inputFileScanner = new Scanner(inputFile)) {
            String[] priceStrings = inputFileScanner.nextLine().split(" ");

            int[] prices = new int[priceStrings.length];
            for (int i = 0; i < priceStrings.length; i++) {
                prices[i] = Integer.parseInt(priceStrings[i]);
            }

            int discountPercentage = inputFileScanner.nextInt();

            return new DiscntInputData(prices, discountPercentage);
        }
    }

    private static DiscntOutputData solve(DiscntInputData inputData) {
        int[] prices = inputData.getPrices();
        int numberOfDiscountedItems = prices.length / 3;

        // Sort by price in descending order.
        MergeSort.sort(prices);

        double minPurchaseSum = 0;
        for (int i = 0; i < prices.length; i++) {
            if (i < numberOfDiscountedItems) {
                minPurchaseSum += prices[i] * ((100.0 - inputData.getDiscountPercentage()) / 100);
            }
            else {
                minPurchaseSum += prices[i];
            }
        }

        return new DiscntOutputData(minPurchaseSum);
    }

    private static void writeOutput(String outputFileName, DiscntOutputData outputData) throws IOException {
        DecimalFormatSymbols numberFormatSymbols = new DecimalFormatSymbols();
        numberFormatSymbols.setDecimalSeparator('.');
        DecimalFormat numberFormat = new DecimalFormat("0.00", numberFormatSymbols);
        numberFormat.setGroupingUsed(false);

        try (Writer outputFileWriter = new FileWriter(outputFileName)) {
            outputFileWriter.write(numberFormat.format(outputData.getMinPurchaseSum()));
        }
    }
}
