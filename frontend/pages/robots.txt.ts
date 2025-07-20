import { type GetServerSideProps } from "next";

export const getServerSideProps: GetServerSideProps = async ({ res }) => {
  res.setHeader("Content-Type", "text/plain");
  res.write(`User-agent: *\nAllow: /\n`);
  res.end();
  return { props: {} };
};

export default function Robots() {
  return null; // never rendered
}
