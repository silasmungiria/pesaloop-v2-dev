// @/hooks/useRefresh.ts
import { useState, useCallback } from "react";

// Type the fetchData parameter as a function that returns a Promise<void>
export const useRefresh = (fetchData: () => Promise<void>) => {
  const [fetching, setFetching] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = useCallback(async () => {
    if (fetching || refreshing) {
      // Prevent re-triggering if already fetching or refreshing
      return;
    }

    setRefreshing(true);
    setFetching(true);
    try {
      await fetchData();
    } catch (error) {
      console.error("Error refreshing data:", error);
    } finally {
      setFetching(false);
      setRefreshing(false);
    }
  }, [fetchData, fetching, refreshing]);

  return { fetching, refreshing, onRefresh };
};
