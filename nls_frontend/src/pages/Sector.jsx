import { useState, useEffect } from "react";
import { fetchSectorWiseSymbol, fetchTopSharePrice  } from "../services/chartService";
import SectorContainer from "../components/SectorContainer";
import Breadcrumbs from './../components/Breadcrumbs';

const Sector = () =>{
    const [sectorData, setSectorData] = useState([]);
    const [priceDataDSE, setPriceDataDSE] = useState([]);
    const [priceDataCSE, setPriceDataCSE] = useState([]);
    const [sectorCombined, setSectorCombined] = useState([]);

    useEffect(() => {
        let interval;
        const loadData = async () => {
            try {
                const sectorResp = await fetchSectorWiseSymbol();
                setSectorData(sectorResp);
                const dseResp = await fetchTopSharePrice("DSE");
                setPriceDataDSE(dseResp)
                const cseResp = await fetchTopSharePrice("CSE");
                setPriceDataCSE(cseResp)
            } catch (err) {
             console.error("Error fetching:", err);
            } 
        };
        loadData();
        interval = setInterval(() => {
            loadData();
        }, 10000); // 10,000 ms = 10 sec

        // Cleanup interval on component unmount
        return () => clearInterval(interval);
        }, []);

    useEffect(() => {
      if (!sectorData.length) return;

      const calcTotals = (prices, market) =>
        sectorData.map(({ sector, symbols }) => {
          const totalvolume = symbols.reduce((sum, s) => {
            const found = prices.find((p) => p.symbol === s);
            return sum + (found ? parseFloat(found.volume || 0) : 0);
          }, 0);

          const totalvalue = symbols.reduce((sum, s) => {
            const found = prices.find((p) => p.symbol === s);
            return sum + (found ? parseFloat(found.value_mn || 0) : 0);
          }, 0);

          return { sector, market, totalvolume, totalvalue };
        });

      const dseTotals = calcTotals(priceDataDSE, "DSE");
      const cseTotals = calcTotals(priceDataCSE, "CSE");

      // Merge DSE & CSE data by sector for charting
      const merged = sectorData.map(({ sector }) => {
        const dse = dseTotals.find((d) => d.sector === sector);
        const cse = cseTotals.find((d) => d.sector === sector);
        return {
          sector,
          DSE_Volume: dse ? dse.totalvolume : 0,
          CSE_Volume: cse ? cse.totalvolume : 0,
          DSE_Value: dse ? dse.totalvalue : 0,
          CSE_Value: cse ? cse.totalvalue : 0,
        };
      });

      setSectorCombined(merged);
    }, [sectorData, priceDataDSE, priceDataCSE]);

    return (
      <>
        <Breadcrumbs folder="Market" page="Sector Info" />
        <div className="container-fluid py-5">
          <div className="container">
            {sectorCombined ? (
              <div className="row g-5">
                <div className="col-lg-12">
                  <SectorContainer
                    title="Sector-wise Volume (DSE vs CSE)"
                    data={sectorCombined}
                    metric="volume"
                  />
                </div>
                <div className="col-lg-12 mt-5">
                  <SectorContainer
                    title="Sector-wise Value (DSE vs CSE)"
                    data={sectorCombined}
                    metric="value"
                  />
                </div>
              </div>
            ) : (
              <div className="text-center p-5">
                <div
                  className="spinner-border text-primary mb-3"
                  role="status"
                ></div>
              </div>
            )}
          </div>
        </div>
      </>
    );
}

export default Sector