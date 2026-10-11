const IssueStatus  = ({title,indexData}) =>{
    return (
      <>
        <div className="issue-status-panel text-center">
          <h5 className="text-primary fw-bold mb-2">{title}</h5>
          <div className="table-responsive w-100">
            <table className="table table-bordered w-100 text-center mb-0 issue-status-table">
              <thead>
                <tr>
                  <th className="text-success">Advanced ↑</th>
                  <th className="text-danger">Declined ↓</th>
                  <th className="text-warning">Unchanged ↔</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="text-success">{indexData?.advance ?? "-"}</td>
                  <td className="text-danger">{indexData?.decline ?? "-"}</td>
                  <td className="text-warning">{indexData?.unchange ?? "-"}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </>
    );
}

export default IssueStatus ;