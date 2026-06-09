const DJANGO_BASE  = import.meta.env.VITE_API_BASE    ?? '';
const FASTAPI_BASE = import.meta.env.VITE_FASTAPI_BASE ?? '';

// Fetching Board index data time wise
export async function fetchMinutesIndex(id) {
  try {
    // ✅ Make sure the path is correct relative to your public folder
    const response = await fetch(`${DJANGO_BASE}/minutes_index/${id}`);

    // ✅Check once and only once
    if (!response.ok) {
      console.error("DSE fetch failed with status:", response.status);
      return { error: `Server responded with status ${response.status}` };
    }

    // ✅ Parse the body only ONCE
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching chart data:", error);
    return { error: "Network error or server not reachable" };
  }
}

// Fetching Market index data index wise
export async function fetchMarketInfo(id) {
  try {
    const response = await fetch(`${DJANGO_BASE}/market_info/${id}`);
    
    if (!response.ok) {
      console.error("DSE fetch failed with status:", response.status);
      return { error: `Server responded with status ${response.status}` };
    }
    
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching dse index data:", error);
    return { error: "Network error or server not reachable" };
  }
}

// Fetching Market index data index wise
export async function fetchMarketIndex(id) {
  try {
    const response = await fetch(`${DJANGO_BASE}/market_index/${id}`);
    
    if (!response.ok) {
      console.error("DSE fetch failed with status:", response.status);
      return { error: `Server responded with status ${response.status}` };
    }
    
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching dse index data:", error);
    return { error: "Network error or server not reachable" };
  }
}
// Fetching DSE ticker data instruemnt wise
export async function fetchTickerPrice(id) {
  try {
    // ✅ Make sure the path is correct relative to your public folder
    const response = await fetch(`${DJANGO_BASE}/ticker_price/${id}`);

    // ✅Check once and only once
    if (!response.ok) {
      console.error("DSE fetch failed with status:", response.status);
      return { error: `Server responded with status ${response.status}` };
    }

    // ✅ Parse the body only ONCE
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching ticker data:", error);
    return { error: "Network error or server not reachable" };
  }
}

// Fetching DSE index data index wise
export async function fetchIPO() {
  try {
    // ✅ Make sure the path is correct relative to your public folder
    const response = await fetch("${FASTAPI_BASE}/ipo_offer");

    // ✅Check once and only once
    if (!response.ok) {
      console.error("DSE fetch failed with status:", response.status);
      return { error: `Server responded with status ${response.status}` };
    }

    // ✅ Parse the body only ONCE
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching ipo data:", error);
    return { error: "Network error or server not reachable" };
  }
}
// Fetching DSE News
export async function fetchDSENews() {
  try {
    // ✅ Make sure the path is correct relative to your public folder
    const response = await fetch("${FASTAPI_BASE}/dse_news");

    // ✅Check once and only once
    if (!response.ok) {
      console.error("DSE fetch failed with status:", response.status);
      return { error: `Server responded with status ${response.status}` };
    }

    // ✅ Parse the body only ONCE
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching dse news data:", error);
    return { error: "Network error or server not reachable" };
  }
};

// Fetching CSE News
export async function fetchCSENews() {
  try {
    // ✅ Make sure the path is correct relative to your public folder
    const response = await fetch("${FASTAPI_BASE}/cse_news");

    // ✅Check once and only once
    if (!response.ok) {
      console.error("CSE fetch failed with status:", response.status);
      return { error: `Server responded with status ${response.status}` };
    }

    // ✅ Parse the body only ONCE
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching cse news data:", error);
    return { error: "Network error or server not reachable" };
  }
};
// Fetching DSE latest share price instruemnt wise
export async function fetchTopSharePrice(id) {
  try {
    // ✅ Make sure the path is correct relative to your public folder
    const response = await fetch(`${DJANGO_BASE}/top_share_price_by/${id}`);

    // ✅Check once and only once
    if (!response.ok) {
      console.error("DSE fetch failed with status:", response.status);
      return { error: `Server responded with status ${response.status}` };
    }

    // ✅ Parse the body only ONCE
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching share data:", error);
    return { error: "Network error or server not reachable" };
  }
}

// Fetching DSE Sector Wise symbols
export async function fetchSectorWiseSymbol() {
  try {
    // ✅ Make sure the path is correct relative to your public folder
    const response = await fetch("${DJANGO_BASE}/sector_wise_inst");

    // ✅Check once and only once
    if (!response.ok) {
      console.error("DSE fetch failed with status:", response.status);
      return { error: `Server responded with status ${response.status}` };
    }

    // ✅ Parse the body only ONCE
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching sector data:", error);
    return { error: "Network error or server not reachable" };
  }
}