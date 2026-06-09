const BASE = import.meta.env.VITE_API_BASE ?? '';

export const getPlainText = (htmlString) => {
  const doc = new DOMParser().parseFromString(htmlString, "text/html");
  return doc.body.textContent || "";
};

export const getAbout = async () => {
  try {
    const response = await fetch(`${BASE}/about/`, {
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
      url = `${BASE}/about_image/`;
    } else {
      url = `${BASE}/about_image/${id}`;
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
    const response = await fetch(`${BASE}/slider/`, {
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
      url = `${BASE}/service/`;
    } else {
      url = `${BASE}/service/${id}`;
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
    const response = await fetch(`${BASE}/product/${id}`, {
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
      url = `${BASE}/feature/`;
    } else {
      url = `${BASE}/feature/${id}`;
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
      url = `${BASE}/offer/`;
    } else {
      url = `${BASE}/offer/${id}`;
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
      url = `${BASE}/board_member/`;
    } else {
      url = `${BASE}/board_member/${id}`;
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
      url = `${BASE}/mancom/`;
    } else {
      url = `${BASE}/mancom/${id}`;
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
    const response = await fetch(`${BASE}/tech/`, {
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
      url = `${BASE}/event/`;
    } else {
      url = `${BASE}/event/${id}`;
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
      url = `${BASE}/market_news/`;
    } else {
      url = `${BASE}/market_news/${id}`;
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
    const response = await fetch(`${BASE}/client/`, {
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
    const response = await fetch(`${BASE}/faq/`, {
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
    const response = await fetch(`${BASE}/privacy-policy/`, {
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
    const response = await fetch(`${BASE}/ipo/`, {
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
      url = `${BASE}/branch/`;
    } else {
      url = `${BASE}/branch/${id}`;
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
    const response = await fetch(`${BASE}/top_share_price_by/${id}`);

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
    const response = await fetch(`${BASE}/categories/`, {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};