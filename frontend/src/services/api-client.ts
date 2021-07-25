import {
  checkDecodedObject,
  IGetUserVars,
  IGraphQLClient,
  MUser,
} from './data-models';
import { DocumentNode, useQuery } from '@apollo/client';
import * as t from 'io-ts';
import * as query from './queries';

export function useGraphQL<T, V>(
  query: DocumentNode,
  typeC: t.Type<T>,
  vars?: V
) {
  const { loading, data } = useQuery<T>(query, { variables: vars });
  console.log('Data:', data);
  /* debugger */
  if (!loading) {
    const response = checkDecodedObject(typeC.decode(data));
    return { loading, response };
  } else {
    return { loading, response: null };
  }
}

export class IApiClient implements IGraphQLClient {
  addUser(name: string, email: string, password: string) {
    return { success: false, errors: ['Method not implemented.'] };
  }
  getUser(email: string) {
    return { success: false, errors: ['Method not implemented.'], info: null };
  }

  addProject(title: string, description?: string) {
    return { success: false, errors: ['Method not implemented.'] };
  }
  getProject(email: string) {
    return { success: false, errors: ['Method not implemented.'], info: null };
  }

  addIssue(
    project_id: string,
    title: string,
    description?: string,
    assigned_to?: string,
    due_date?: number,
    severity?: string,
    flag?: string,
    tags?: string[],
    classification?: string,
    reproducible?: string
  ) {
    return { success: false, errors: ['Method not implemented.'] };
  }
  getIssue(email: string) {
    return { success: false, errors: ['Method not implemented.'], info: null };
  }
}
