import React from 'react';
import { IGetUserResponse, MGetUserResponse } from '../../entities/data-models';
import { GET_USERS } from '../../entities/queries';
import useGraphQL from '../../hooks/useGraphQL';

const Dashboard: React.FC = () => {
  const { loading, response } = useGraphQL<IGetUserResponse, {}>(
    GET_USERS,
    MGetUserResponse
  );

  if (!loading) {
    console.log(response);
  }

  return (
    <div>
      <h1>This is the Dashboard</h1>
    </div>
  );
};

export default Dashboard;
