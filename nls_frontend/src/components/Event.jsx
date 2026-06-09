import { useParams } from "react-router-dom";

const Event = ()=>{
    const { id } = useParams();
    return (
      <>
        <div>
          <h2>Event ID: {id}</h2>
          {/* You can fetch event data here based on the ID */}
        </div>
      </>
    );
}

export default Event;