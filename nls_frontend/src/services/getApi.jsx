const BASE = import.meta.env.VITE_API_BASE ?? '';

export const getPlainText = (htmlString) => {
  const doc = new DOMParser().parseFromString(htmlString, "text/html");
  return doc.body.textContent || "";
};

export const getAbout = async () => {
  try {
    const response = await fetch(`${BASE}/api/about/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getAboutImage = async (id) => {
 var url;
  try {
    if (id === null) {
      url = `${BASE}/api/about_image/`;
    } else {
      url = `${BASE}/api/about_image/${id}`;
    }
    const response = await fetch(url, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getCarousal = async () => {
  try {
    const response = await fetch(`${BASE}/api/slider/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getSplash = async () => {
  try {
    const response = await fetch(`${BASE}/api/splash/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getServices = async (id) => {
  var url;
  try {
    if (id === null) {
      url = `${BASE}/api/service/`;
    } else {
      url = `${BASE}/api/service/${id}`;
    }
    const response = await fetch(url, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getProducts = async (id) => {
  try {
    const response = await fetch(`${BASE}/api/product/${id}`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getFeatures = async (id) => {
  var url;
  try {
    if (id === null) {
      url = `${BASE}/api/feature/`;
    } else {
      url = `${BASE}/api/feature/${id}`;
    }
    const response = await fetch(url, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getOffers = async (id) => {
  var url;
  try {
    if (id === null) {
      url = `${BASE}/api/offer/`;
    } else {
      url = `${BASE}/api/offer/${id}`;
    }
    const response = await fetch(url, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getBoardMembers = async (id) => {
  var url;
  try {
    if (id === null) {
      url = `${BASE}/api/board_member/`;
    } else {
      url = `${BASE}/api/board_member/${id}`;
    }
    const response = await fetch(url, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getManComs = async (id) => {
  var url;
  try {
    if (id === null) {
      url = `${BASE}/api/mancom/`;
    } else {
      url = `${BASE}/api/mancom/${id}`;
    }
    const response = await fetch(url, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getTeams = async () => {
  try {
    const response = await fetch(`${BASE}/api/tech/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getEvents = async (id) => {
  var url;
  try {
    if (id === null) {
      url = `${BASE}/api/event/`;
    } else {
      url = `${BASE}/api/event/${id}`;
    }
    const response = await fetch(url, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getMarketNews = async (id) => {
  var url;
  try {
    if (id === null) {
      url = `${BASE}/api/market_news/`;
    } else {
      url = `${BASE}/api/market_news/${id}`;
    }
    const response = await fetch(url, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getClients = async () => {
  try {
    const response = await fetch(`${BASE}/api/client/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getFaqs = async () => {
  try {
    const response = await fetch(`${BASE}/api/faq/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getPolicy = async () => {
  try {
    const response = await fetch(`${BASE}/api/privacy-policy/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getIPO = async () => {
  try {
    const response = await fetch(`${BASE}/api/ipo/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getBranches = async (id) => {
 var url;
  try {
    if (id === null) {
      url = `${BASE}/api/branch/`;
    } else {
      url = `${BASE}/api/branch/${id}`;
    }
    const response = await fetch(url, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

// Fetching DSE latest share price instruemnt wise
export const fetchTopSharePrice = async (id)=> {
  try {
    // ✅ Make sure the path is correct relative to your public folder
    const response = await fetch(`${BASE}/api/top_share_price_by/${id}`);

    // ✅Check once and only once
    if (!response.ok) {
      throw new Error("Failed to fetch ticker data");
    }

    // ✅ Parse the body only ONCE
    const jsonData = await response.json();
    return jsonData;
  } catch (error) {
    console.error("Error fetching ticker data:", error);
    return {};
  }
}

export const getFilesByCategories = async () => {
  try {
    const response = await fetch(`${BASE}/api/categories/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};