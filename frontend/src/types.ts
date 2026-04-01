export type Student = {
  id: number;
  name: string;
  university: string;
  faculty: string;
  graduation_year: number;
  skills: string[];
  desired_industries: string[];
  self_pr: string;
  last_login: string;
};

export type ScoutMessage = {
  id: number;
  student_id: number;
  student_name: string;
  student_university: string;
  subject: string;
  status: "pending" | "opened" | "accepted" | "declined";
  sent_at: string;
  responded_at: string | null;
};

export type DashboardStats = {
  total_scouts_sent: number;
  scouts_opened: number;
  scouts_accepted: number;
  scouts_declined: number;
  open_rate: number;
  accept_rate: number;
  active_students: number;
  new_students_this_week: number;
};
