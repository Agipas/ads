public class MergeSort {

    public static void sort(long[] array) {
        long[] mergeResults = new long[array.length];
        mergeSortRecursive(array, mergeResults, 0, array.length - 1);
    }

    private static void mergeSortRecursive(long[] array, long[] mergeResults, int left, int right) {
        if (left < right) {
            int center = (left + right) / 2;
            mergeSortRecursive(array, mergeResults, left, center);
            mergeSortRecursive(array, mergeResults, center + 1, right);
            merge(array, mergeResults, left, center + 1, right);
        }
    }

    private static void merge(long[] array, long[] mergeResults, int leftBegin, int rightBegin, int rightEnd) {
        int leftEnd = rightBegin - 1;
        int leftReadPos = leftBegin;
        int rightReadPos = rightBegin;
        int resultWritePos = leftBegin;

        while (leftReadPos <= leftEnd && rightReadPos <= rightEnd) {
            if (array[leftReadPos] < (array[rightReadPos])) {
                mergeResults[resultWritePos++] = array[leftReadPos++];
            } else {
                mergeResults[resultWritePos++] = array[rightReadPos++];
            }
        }

        while (leftReadPos <= leftEnd) {
            mergeResults[resultWritePos++] = array[leftReadPos++];
        }

        while (rightReadPos <= rightEnd) {
            mergeResults[resultWritePos++] = array[rightReadPos++];
        }

        for (int i = leftBegin; i <= rightEnd; i++) {
            array[i] = mergeResults[i];
        }
    }

}
