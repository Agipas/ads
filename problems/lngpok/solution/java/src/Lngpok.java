import java.io.*;
import java.util.Arrays;
import java.util.Scanner;

public class Lngpok {

    public static void main(String[] args) throws IOException {
        String inputFileName = args.length >= 2 ? args[0] : "lngpok.in";
        String outputFileName = args.length >= 2 ? args[1] : "lngpok.out";

        LngpokInputData inputData = readInput(inputFileName);
        LngpokOutputData outputData = solve(inputData);
        writeOutput(outputFileName, outputData);
    }

    private static LngpokInputData readInput(String inputFileName) throws FileNotFoundException {
        File inputFile = new File(inputFileName);

        try (Scanner inputFileScanner = new Scanner(inputFile)) {
            String[] cardStrings = inputFileScanner.nextLine().split(" ");

            int[] cards = new int[cardStrings.length];
            for (int i = 0; i < cardStrings.length; i++) {
                cards[i] = Integer.parseInt(cardStrings[i]);
            }

            return new LngpokInputData(cards);
        }
    }

    private static LngpokOutputData solve(LngpokInputData inputData) {
        int[] sortedCards = inputData.getCards();
        MergeSort.sort(sortedCards);

        int jokerBudget = countJokers(sortedCards);
        int[] sortedUniqueNonJokers = getUniqueNonJokerCards(sortedCards);

        int maxSequenceLengthSoFar = jokerBudget;

        // Finding the pair (sequenceBegin, sequenceEnd) that gives us the longest sequence that fits our budget.
        for (int sequenceBegin = 0; sequenceBegin < sortedUniqueNonJokers.length; sequenceBegin++) {

            // To locate 'sequenceEnd', we could just do a simple loop from N down to 'sequenceBegin'.
            // But that would lead to O(N^2) time in the worst case.
            // Instead, we'll use binary search here to locate the right bound in O(log N).
            // Therefore, the total complexity for search would be O(N) * O(log N) = O(N log N).
            int left = sequenceBegin;
            int right = sortedUniqueNonJokers.length - 1;

            while (left < right) {
                int candidateSequenceEnd = (left + right + 1) / 2;
                if (candidateSequenceEnd > right) {
                    break;
                }

                if (!canFillSequenceWithJokers(sortedUniqueNonJokers, jokerBudget, sequenceBegin, candidateSequenceEnd)) {
                    right = candidateSequenceEnd - 1;
                }
                else {
                    left = candidateSequenceEnd;
                }
            }

            int sequenceEnd = right;
            int longestSequenceWithThisLeftBound = (sequenceEnd - sequenceBegin + 1) + jokerBudget;
            if (longestSequenceWithThisLeftBound > maxSequenceLengthSoFar) {
                maxSequenceLengthSoFar = longestSequenceWithThisLeftBound;
            }
        }

        return new LngpokOutputData(maxSequenceLengthSoFar);
    }

    private static int countJokers(int[] sortedCards) {
        for (int i = 0; i < sortedCards.length; i++) {
            if (sortedCards[i] != 0) {
                return i;
            }
        }
        return sortedCards.length;
    }

    private static int[] getUniqueNonJokerCards(int[] sortedCards) {
        int[] uniquesBuffer = new int[sortedCards.length];
        int currentCard = 0;
        int uniqueCardCount = 0;

        for (int card : sortedCards) {
            if (card != currentCard) {
                uniquesBuffer[uniqueCardCount++] = card;
                currentCard = card;
            }
        }

        return Arrays.copyOfRange(uniquesBuffer, 0, uniqueCardCount);
    }

    private static boolean canFillSequenceWithJokers(int[] sortedUniqueNonJokers, int jokerBudget, int sequenceBegin, int candidateSequenceEnd) {
        return getJokerCost(sortedUniqueNonJokers, sequenceBegin, candidateSequenceEnd) <= jokerBudget;
    }

    private static int getJokerCost(int[] sortedUniqueNonJokers, int left, int right) {
        return (sortedUniqueNonJokers[right] - sortedUniqueNonJokers[left] - 1) - (right - left - 1);
    }

    private static void writeOutput(String outputFileName, LngpokOutputData outputData) throws IOException {
        try (Writer outputFileWriter = new FileWriter(outputFileName)) {
            outputFileWriter.write(String.valueOf(outputData.getLongestSequenceLength()));
        }
    }
}
