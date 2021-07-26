import { gql } from '@apollo/client';

export const GET_USER = gql`
  query GetUser($email: String!) {
    getUser(email: $email) {
      success
      errors
      info {
        id
        name
        email
      }
    }
  }
`;

export const GET_USERS = gql`
  query {
    getUsers {
      success
      errors
      info {
        id
        name
        email
      }
    }
  }
`;

export const GET_PROJECT = gql`
  query GetProject($id: ID!) {
    getProject(id: $id) {
      success
      errors
      info {
        id
        title
        description
      }
    }
  }
`;

export const GET_ISSUE = gql`
  query GetIssue($id: ID!) {
    getIssue(id: $id) {
      success
      errors
      info {
        id
        project_id
        title
        description
        assigned_to
        reported_date
        due_date
        severity
        flag
        tags
        classification
        reproducible
        project
        assigned_user
      }
    }
  }
`;
