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

export const SEARCH_USERS = gql`
  query SearchUsers($name: String!) {
    searchUsers(email: $email) {
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

export const SEARCH_PROJECTS = gql`
  query SearchProjects($title: String!) {
    searchProjects(title: $title) {
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

export const SEARCH_ISSUES = gql`
  query SearchIssues(
    $project_id: String
    $title: String
    $description: String
    $assigned_to: String
    $reported_date: String
    $due_date: String
    $severity: String
    $flag: String
    $classification: String
    $reproducible: String
  ) {
    searchIssues(
      project_id: $project_id
      title: $title
      description: $description
      assigned_to: $assigned_to
      reported_date: $reported_date
      due_date: $due_date
      severity: $severity
      flag: $flag
      classification: $classification
      reproducible: $reproducible
    ) {
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
