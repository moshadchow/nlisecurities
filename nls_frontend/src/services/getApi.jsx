export const getPlainText = (htmlString) => {
  const doc = new DOMParser().parseFromString(htmlString, "text/html");
  return doc.body.textContent || "";
};

export const getAbout = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/about/", {
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
      url = "http://127.0.0.1:8000/about_image/";
    } else {
      url = `http://127.0.0.1:8000/about_image/${id}`;
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
    const response = await fetch("http://127.0.0.1:8000/slider/", {
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
      url = "http://127.0.0.1:8000/service/";
    } else {
      url = `http://127.0.0.1:8000/service/${id}`;
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
    const response = await fetch(`http://127.0.0.1:8000/product/${id}`, {
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
      url = "http://127.0.0.1:8000/feature/";
    } else {
      url = `http://127.0.0.1:8000/feature/${id}`;
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
      url = "http://127.0.0.1:8000/offer/";
    } else {
      url = `http://127.0.0.1:8000/offer/${id}`;
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
      url = "http://127.0.0.1:8000/board_member/";
    } else {
      url = `http://127.0.0.1:8000/board_member/${id}`;
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
      url = "http://127.0.0.1:8000/mancom/";
    } else {
      url = `http://127.0.0.1:8000/mancom/${id}`;
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
    const response = await fetch("http://127.0.0.1:8000/tech/", {
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
      url = "http://127.0.0.1:8000/event/";
    } else {
      url = `http://127.0.0.1:8000/event/${id}`;
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
      url = "http://127.0.0.1:8000/market_news/";
    } else {
      url = `http://127.0.0.1:8000/market_news/${id}`;
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
    const response = await fetch("http://127.0.0.1:8000/client/", {
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
    const response = await fetch("http://127.0.0.1:8000/faq/", {
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
    const response = await fetch("http://127.0.0.1:8000/privacy-policy/", {
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
    const response = await fetch("http://127.0.0.1:8000/ipo/", {
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
      url = "http://127.0.0.1:8000/branch/";
    } else {
      url = `http://127.0.0.1:8000/branch/${id}`;
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
    const response = await fetch(`http://127.0.0.1:8000/top_share_price_by/${id}`);

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
    const response = await fetch("http://127.0.0.1:8000/categories/", {
      method: "GET",
    });
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};